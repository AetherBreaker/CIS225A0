import json
import os
import re

DATALOC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")


def recurse_dir_search(filetarget: str, current_directory: str = DATALOC) -> str:
    """This is just a custom function for recursively searching the entire current directory
    for the inputed file, including searching through all subfolders.

    Reused from my other projects.
    """
    validextension = re.compile(r"\.[a-zA-Z]{2,4}$")
    path = current_directory
    dirlist = os.listdir(path)
    for filename in dirlist:
        if filename == filetarget:
            path = os.path.join(current_directory, filetarget)
            return path
        elif not validextension.search(filename):
            try:
                return recurse_dir_search(filetarget, os.path.join(path, filename))
            except FileNotFoundError:
                continue
    raise (FileNotFoundError)


if __name__ == "__main__":
    userdata = {}

    datachanged = False

    try:
        fpath = recurse_dir_search("userdata.json")
        with open(fpath, "rb") as f:
            userdata = json.loads(f.read().decode())
    except FileNotFoundError:
        userdata = {}

    firstname = input("Please enter your first name: ")
    lastname = input("Please enter your last name: ")

    if f"{firstname}{lastname}" in userdata:
        print(
            "\n".join(
                f"""
                {movie['title']}:
                \tDirector: {movie['director']}
                \tRelease Year: {movie['releaseyear']}
                \tIMDB Rating: {movie['imdbrating']}
                \tRotten Tomatoes Rating: {movie['tomatoesrating']}
                \tMPAA Rating: {movie['mpaarating']}"""
                for movie in userdata[f"{firstname}{lastname}"]["movies"]
            )
        )
    else:
        print("Please input your top 5 favorite movies in descending order.")
        userdata[f"{firstname}{lastname}"] = {"movies": []}
        for i in range(5):
            moviedata = {
                "title": "",
                "director": "",
                "releaseyear": None,
                "imdbrating": None,
                "tomatoesrating": None,
                "mpaarating": "",
            }

            moviedata["title"] = input(f"Movie #{i+1} Title: ")
            moviedata["director"] = input(f"Movie #{i+1} Director: ")
            while not moviedata["releaseyear"]:
                try:
                    moviedata["releaseyear"] = int(
                        input(f"Movie #{i+1} Release Year: ")
                    )
                except ValueError:
                    print("Please enter a valid year.")
            while not moviedata["imdbrating"]:
                try:
                    rating = int(input(f"Movie #{i+1} IMDB Rating: "))
                    if rating < 0 or rating > 5:
                        raise ValueError
                    moviedata["imdbrating"] = rating
                except ValueError:
                    print("Please enter a valid rating.")
            while not moviedata["tomatoesrating"]:
                try:
                    rating = int(input(f"Movie #{i+1} Tomatoes Rating: "))
                    if rating < 0 or rating > 5:
                        raise ValueError
                    moviedata["tomatoesrating"] = rating
                except ValueError:
                    print("Please enter a valid rating.")
            moviedata["mpaarating"] = input(
                f"Movie #{i+1} MPAA Rating (eg: PG, PG-13, R, etc.): "
            )

            userdata[f"{firstname}{lastname}"]["movies"].append(moviedata)
            datachanged = True

    if datachanged:
        try:
            fpath = recurse_dir_search("userdata.json")
            with open(fpath, "wb") as f:
                f.write(json.dumps(userdata, indent=4).encode())
        except FileNotFoundError:
            with open(os.path.join(DATALOC, "userdata.json"), "wb") as f:
                f.write(json.dumps(userdata, indent=4).encode())
