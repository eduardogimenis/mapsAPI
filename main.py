import googlemaps
import pandas as pd
import tkinter as tk
from tkinter import ttk
import time
import os
from dotenv import load_dotenv

# Load API key from environment variable
load_dotenv()
API_KEY = "AIzaSyAeOL_45HwFP4APyRYk9LWT6afSdtpOE5g"

if not API_KEY:
    raise ValueError("Google Maps API key is missing. Add it to a .env file as GOOGLE_MAPS_API_KEY.")

# Initialize Google Maps client
gmaps = googlemaps.Client(key=API_KEY)

def search_places(location, radius, keyword):
    """
    Search for places within a specified radius around a location using a keyword.
    """
    results = []
    next_page_token = None

    while True:
        response = gmaps.places_nearby(
            location=location,
            radius=radius,
            keyword=keyword,
            page_token=next_page_token
        )
        results.extend(response.get("results", []))

        # Check if there's another page of results
        next_page_token = response.get("next_page_token")
        if not next_page_token:
            break

        # Google Maps API requires a short delay between paginated requests
        time.sleep(2)

    return results

def get_place_details(place_id):
    """
    Get detailed information about a place.
    """
    details = gmaps.place(place_id=place_id)
    result = details.get("result", {})
    phone_number = result.get("formatted_phone_number", None)
    return phone_number

def export_to_csv(data, filename="beauty_salons.csv"):
    """
    Export data to a CSV file.
    """
    if not data:
        print("No data to export.")
        return

    # Convert list of dictionaries to a DataFrame
    df = pd.DataFrame(data)

    # Save to CSV
    df.to_csv(filename, index=False)
    print(f"Data successfully exported to {filename}.")

def run_app():
    def search_and_export():
        try:
            # Get input values
            location = location_entry.get()
            radius = int(radius_entry.get())
            lat, lng = map(float, location.split(","))  # Parse lat, lng
            city = city_entry.get().strip()  # Get the city name
            
            # Build the search keyword: "beauty salon" with city appended if provided
            keyword = f"beauty salon {city}" if city else "beauty salon"
            
            # Update status label
            status_label.config(text="Fetching beauty salons...", fg="white")
            root.update()  # Update GUI
            
            results = search_places((lat, lng), radius, keyword)
            data = []

            # Fetch phone numbers and create URLs for each place
            for i, place in enumerate(results):
                place_id = place.get("place_id")
                phone_number = get_place_details(place_id)
                place_url = f"https://www.google.com/maps/place/?q=place_id:{place_id}"

                data.append({
                    "Name": place.get("name"),
                    "Address": place.get("vicinity"),
                    "Rating": place.get("rating"),
                    "Phone": phone_number,
                    "URL": place_url,
                })

                # Update progress in status label
                status_label.config(
                    text=f"Fetching details... {i + 1}/{len(results)}", fg="white"
                )
                root.update()

            # Determine CSV filename based on city name
            if city:
                # Replace spaces with underscores to avoid issues in filenames
                filename = f"beauty_salons_{city.replace(' ', '_')}.csv"
            else:
                filename = "beauty_salons.csv"

            # Export results using the dynamic filename
            export_to_csv(data, filename)
            
            # Update status label with number of entries
            status_label.config(
                text=f"Exported {len(data)} entries to {filename}", fg="white"
            )
        except Exception as e:
            status_label.config(text=f"Error: {str(e)}", fg="red")


    # Create the main application window
    root = tk.Tk()
    root.title("Beauty Salon Finder")
    root.configure(bg="black")

    # Create and place widgets
    tk.Label(root, text="Enter Location (latitude, longitude):", bg="black", fg="white").grid(row=0, column=0, padx=10, pady=10)
    location_entry = tk.Entry(root, width=30)
    location_entry.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(root, text="Radius (in meters):", bg="black", fg="white").grid(row=1, column=0, padx=10, pady=10)
    radius_entry = tk.Entry(root, width=30)
    radius_entry.grid(row=1, column=1, padx=10, pady=10)

    # New: City Name input field
    tk.Label(root, text="City Name (optional):", bg="black", fg="white").grid(row=2, column=0, padx=10, pady=10)
    city_entry = tk.Entry(root, width=30)
    city_entry.grid(row=2, column=1, padx=10, pady=10)

    # Button to trigger search
    search_button = tk.Button(root, text="Search and Export", command=search_and_export)
    search_button.grid(row=3, column=0, columnspan=2, pady=10)

    # Status label
    status_label = tk.Label(root, text="", bg="black", fg="white")
    status_label.grid(row=4, column=0, columnspan=2, pady=10)

    # Run the application loop
    root.mainloop()

if __name__ == "__main__":
    run_app()
