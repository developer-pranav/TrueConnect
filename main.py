import pandas as pd
from fpdf import FPDF
import json
import os
import sys
from typing import Any, Optional, Set, Tuple
from pathlib import Path
from datetime import datetime


def resource_path(relative_path: str) -> str:
    """
    Get absolute path to resource, works for dev and for PyInstaller.
    """
    if hasattr(sys, "_MEIPASS"):  # Running from the .exe
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def _extract_usernames(data: Any, key: Optional[str] = None) -> Set[str]:
    """Safely extracts usernames from the Instagram data structure."""
    usernames = set()
    
    items_list = data.get(key, []) if key else data

    for item in items_list:
        try:
            username = item["string_list_data"][0]["value"]
            usernames.add(username)
        except (KeyError, IndexError):
            pass
    return usernames


def analyze_instagram_data(
    followers_file: str, following_file: str
) -> Tuple[Set[str], Set[str]]:
    """
    Analyzes Instagram followers and following data to find users who don't follow back
    and fans who are not followed back.
    """
    try:
        with open(followers_file, "r", encoding="utf-8") as f:
            followers_data = json.load(f)

        with open(following_file, "r", encoding="utf-8") as f:
            following_data = json.load(f)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Error: {e.filename} not found. Please ensure the file is in the correct directory.") from e
    except json.JSONDecodeError as e:
        raise ValueError(f"Error: Could not decode JSON from a file. It may be empty or malformed.") from e

    followers = _extract_usernames(followers_data)
    following = _extract_usernames(following_data, "relationships_following")

    not_following_back = following - followers
    fans = followers - following

    return not_following_back, fans


def get_path_from_user(prompt: str) -> str:
    """Prompts the user to drag and drop a file and reads the path from stdin."""
    print(prompt)
    path = input("> ").strip()
    return path.strip('\'"')


def create_pdf_report(not_following_back: Set[str], fans: Set[str]) -> str:
    """Generates a PDF report of the analysis."""
    pdf = FPDF()
    pdf.add_page()

    regular_font_path = resource_path("fonts/DejaVuSans.ttf")
    bold_font_path = resource_path("fonts/DejaVuSans-Bold.ttf")

    pdf.add_font("DejaVu", "", regular_font_path, uni=True)
    pdf.add_font("DejaVu", "B", bold_font_path, uni=True)

    logo_path = resource_path("assets/company_logo.jpg")
    page_width = pdf.w - pdf.l_margin - pdf.r_margin
    
    pdf.set_font("DejaVu", "B", 20)
    pdf.cell(page_width * 0.7, 10, "TrueConnect", 0, 0, "L")

    if os.path.exists(logo_path):
        pdf.image(logo_path, x=pdf.w - pdf.r_margin - 30, y=pdf.get_y() - 2, w=30)
    else:
        pdf.ln(10)

    pdf.ln(15)
    
    def draw_list_in_columns(pdf_instance, title, user_list, color):
        """Helper function to draw a titled list in a 3-column layout."""
        pdf_instance.set_fill_color(color[0], color[1], color[2])
        pdf_instance.ellipse(pdf_instance.get_x(), pdf_instance.get_y() + 3.5, 3, 3, 'F')
        pdf_instance.set_x(pdf_instance.get_x() + 5)

        pdf_instance.set_font("DejaVu", "B", 12)
        pdf_instance.cell(0, 10, f"{title} ({len(user_list)})", 0, 1)
        pdf_instance.set_font("DejaVu", "", 10)

        if not user_list:
            pdf_instance.cell(0, 7, "  None.", 0, 1)
            return

        page_width = pdf_instance.w - pdf_instance.l_margin - pdf_instance.r_margin
        col_width = page_width / 3
        line_height = 7
        num_cols = 3

        start_y = pdf_instance.get_y()
        current_y = start_y

        page_item_index = 0

        sorted_users = sorted(list(user_list))
        
        for i, user in enumerate(sorted_users):
            col_index = page_item_index % num_cols
            row_index = page_item_index // num_cols

            if current_y + (row_index * line_height) > (pdf_instance.h - pdf_instance.b_margin - line_height):
                pdf_instance.add_page()
                current_y = pdf_instance.t_margin
                page_item_index = 0
                col_index = page_item_index % num_cols
                row_index = page_item_index // num_cols

            pdf_instance.set_xy(pdf_instance.l_margin + (col_index * col_width), current_y + (row_index * line_height))
            safe_user = f"- {user}".encode('latin-1', 'replace').decode('latin-1')
            pdf_instance.cell(col_width, line_height, safe_user, 0, 0)
            page_item_index += 1
        
        pdf_instance.set_y(pdf_instance.get_y() + line_height * 2)

    draw_list_in_columns(pdf, "People You Follow Who Don't Follow Back", not_following_back, color=(220, 53, 69))
    pdf.ln(8)
    draw_list_in_columns(pdf, "People You Don't Follow Them Back", fans, color=(40, 167, 69))

    # --- Generate Filename and Save ---
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pdf_filename = f"trueconnect_report_{timestamp}.pdf"

    try:
        downloads_dir = Path.home() / "Downloads"
        downloads_dir.mkdir(exist_ok=True)
        full_path = downloads_dir / pdf_filename
    except Exception:
        # Fallback to the current directory if Downloads folder is not found
        full_path = Path(pdf_filename)

    try:
        pdf.output(full_path)
        return str(full_path)
    except Exception as e:
        raise IOError(f"Failed to create PDF report: {e}") from e


def main():
    """Main function to run the analysis and generate reports."""
    print("\n--- TrueConnect - Instagram Follow Analyzer ---\n")
    
    followers_file = get_path_from_user("\n📄 Give or Drag your followers JSON file here and press Enter:")
    if not followers_file:
        print("Operation cancelled: No followers file provided.", file=sys.stderr)
        sys.exit(1)
    
    following_file = get_path_from_user("\n📄 Give or Drag your following JSON file here and press Enter:")
    if not following_file:
        print("Operation cancelled: No following file provided.", file=sys.stderr)
        sys.exit(1)
    
    print("-" * 20)
    try:
        not_following_back, fans = analyze_instagram_data(followers_file, following_file)

        # --- Console Output ---
        print("🔴 People you follow but don't follow you back:")
        if not_following_back:
            for user in sorted(not_following_back):
                print(f" - {user}")
        else:
            print("   None. Great!")

        print("\n🟢 People who follow you but you don't follow back:")
        if fans:
            for user in sorted(fans):
                print(f" - {user}")
        else:
            print("   None. You follow back everyone who follows you!")

        # --- PDF Export Prompt ---
        print("\n" + "-" * 20)
        while True:
            choice = input("📄 Do you want to download this report as a PDF? (y/n): ").lower().strip()
            if choice in ["y", "yes"]:
                full_filename_path = create_pdf_report(not_following_back, fans)
                print(f"\n✅ Report successfully saved to:\n   {full_filename_path}")
                break
            elif choice in ["n", "no"]:
                print("\n👍 Report not saved. Exiting.")
                break
            else:
                print("Invalid choice. Please enter 'y' or 'n'.")

    except (FileNotFoundError, ValueError) as e:
        print(e, file=sys.stderr)
        sys.exit(1)
    finally:
        # Keep the terminal open so the user can see the output.
        print("\nPress Enter to exit.")
        input()

if __name__ == "__main__":
    main()
