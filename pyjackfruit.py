import requests
import tkinter as tk
from tkinter import messagebox
from io import BytesIO
from PIL import Image, ImageTk

API_KEY = "c27c475407mshf74e48a0f77451bp1007dajsnd881d5c2770d"


def fetch_movie_details(movie_name):
    if not API_KEY:
        raise ValueError("Please put your RapidAPI key in API_KEY.")

    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": "imdb8.p.rapidapi.com"
    }

    search_url = "https://imdb8.p.rapidapi.com/auto-complete"
    r = requests.get(search_url, headers=headers, params={"q": movie_name}, timeout=10)
    data = r.json()

    if "d" not in data or not data["d"]:
        return None

    top = data["d"][0]
    movie_id = top.get("id")

    details_url = "https://imdb8.p.rapidapi.com/title/get-overview-details"
    r = requests.get(
        details_url,
        headers=headers,
        params={"tconst": movie_id, "currentCountry": "IN"},
        timeout=10
    )
    d = r.json()

    title = d.get("title", {}).get("title", top.get("l", ""))
    year = d.get("title", {}).get("year")
    runtime = d.get("title", {}).get("runningTimeInMinutes")
    rating = d.get("ratings", {}).get("rating")
    plot = d.get("plotOutline", {}).get("text")

    genres = ", ".join(d.get("genres", []))

    principals = d.get("principals", [])
    cast_names = []
    for p in principals:
        name_obj = p.get("name")
        if name_obj and "name" in name_obj:
            cast_names.append(name_obj["name"])
    cast = ", ".join(cast_names[:5])

    poster = None
    if isinstance(top.get("i"), dict):
        poster = top["i"].get("imageUrl")
    if not poster:
        poster = d.get("title", {}).get("image", {}).get("url")

    return {
        "title": title,
        "year": year,
        "runtime": runtime,
        "rating": rating,
        "genres": genres,
        "cast": cast,
        "plot": plot,
        "poster": poster
    }


def on_search():
    movie_name = entry.get().strip()
    if not movie_name:
        messagebox.showwarning("Input needed", "Please enter a movie name.")
        return

    def set_output(text):
        output.config(state="normal")
        output.delete("1.0", tk.END)
        output.insert(tk.END, text)
        output.config(state="disabled")

    def clear_poster():
        poster_label.config(image="")
        poster_label.image = None

    set_output("Searching...\n")
    clear_poster()

    try:
        details = fetch_movie_details(movie_name)
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return

    if not details:
        messagebox.showinfo("Not found", "No movies found.")
        set_output("")
        return

    if details.get("poster"):
        try:
            img_data = requests.get(details["poster"], timeout=10).content
            img = Image.open(BytesIO(img_data))
            img.thumbnail((250, 350))
            poster_label.image = ImageTk.PhotoImage(img)
            poster_label.config(image=poster_label.image)
        except:
            clear_poster()

    lines = [
        f"Title:   {details['title']}",
        f"Year:    {details['year']}" if details['year'] else "",
        f"Rating:  {details['rating']}/10" if details['rating'] else "",
        f"Runtime: {details['runtime']} min" if details['runtime'] else "",
        f"Genres:  {details['genres']}" if details['genres'] else "",
        f"Cast:    {details['cast']}" if details['cast'] else "",
        "",
        "Plot:",
        details['plot'] if details['plot'] else ""
    ]

    text = "\n".join(line for line in lines if line)
    set_output(text)


# ---------------- GUI ----------------

root = tk.Tk()
root.title("🎬 Movie Search App")
root.geometry("700x500")

top_frame = tk.Frame(root)
top_frame.pack(pady=15)

tk.Label(top_frame, text="Enter movie name:").pack()
entry = tk.Entry(top_frame, width=40,justify="center")
entry.pack(pady=5)

tk.Button(top_frame, text="Search", command=on_search).pack(pady=15)

poster_label = tk.Label(root,text="ENJOY WATCHING THE MOVIE",font=("Arial",12,"bold"))
poster_label.pack(pady=5)

output = tk.Text(root, wrap="word", state="disabled")
output.pack(fill="both", expand=True, padx=10, pady=10)

entry.bind("<Return>", lambda event: on_search())

root.mainloop()
