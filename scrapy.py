from movies import getMovies
from series import getSeries


askForData = input("Elige la opcion que quieras ver: peliculas, series o ver todo: ")

if(askForData == "peliculas" or askForData == "Peliculas"):
    getMovies()
    print("peliculas")
elif(askForData == "Series" or askForData == "series"):
    getSeries()
    print("series")

else:
    print("Peliculas: ")
    getMovies()
    print("Series: ")
    getSeries()




