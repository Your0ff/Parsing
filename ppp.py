import requests
from bs4 import BeautifulSoup

def get_pizza_menu():

    url = "https://pizza-shlyapa.ru/"

    response = requests.get(url)

    soup = BeautifulSoup(response.text, "lxml")

    data = soup.find_all("div", class_="col-lg-3 col-md-6 mb-4 one-card")

    res = []

    for i in data[1:-52]:

        name = i.find("h4", class_="card-title script").text
        title = i.find_all("p")[1].text
        price = (i.find("div", class_="text-left order-holder").text
                 .replace("				 ", " ")
                 .strip("\n")
                 .replace(" 				", " ")
                 .replace("\n", "").replace(" 						", "\n"))
        url_img = i.find("img", class_="card-img-top").get("src")

        res.append((url_img, name + "\n" + title + "\n\n" + price))

    return(res)

if __name__ == '__main__':
    get_pizza_menu()