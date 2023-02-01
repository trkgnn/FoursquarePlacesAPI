import requests
import pandas as pd
import numpy as np


#Coffee places FSQ Category IDs
cat_id=["13032","13034","13036","11126","13035","13037","17063"]

def find_coordinates (se,nw):
    """Function to get all coordinates with approx 2 km distance in a desired rectangle. se=south east coordinate, nw=north west coordinates"""
    lat_min=se[0]
    lat_max=nw[0]
    lon_min=nw[1]
    lon_max=se[1]
    lons=[]
    lon= lon_min
    check=True
    while check:
        lons.append(round(lon, 2))
        lon=lon+0.02
        if lon>lon_max:
            check=False
    places_ll=[]
    for lon in lons:
        x=True
        lat=lat_min
        while x:
            coordinates=f"{round(lat,2)}"+ "," +f"{lon}"
            places_ll.append(coordinates)
            lat=lat+0.02
            if lat>lat_max:
                x=False
    return places_ll


def get_reviews(place_df):
    """Function taking in a data frame with "fsq_id" column and adding reviews of those IDs to the same dataframe
    """
    all_reviews=[] 
    for num in range(0,len(place_df)):
        try:
            x=str(place_df["fsq_id"][num])
            url = f'https://api.foursquare.com/v3/places/{x}/tips?limit=50&fields=text'

            headers = {
                "accept": "application/json",
                "Authorization": "Your API KEY"
            }

            response = requests.get(url, headers=headers)
            tips_df=pd.json_normalize(response.json())
            reviews=""
            for n in range (0,len(tips_df)):
                reviews=reviews+"// "+tips_df["text"][n]
            all_reviews.append(reviews)
        except Exception as e:
            all_reviews.append("no comment")
            print(f"error {e}")
                   
    place_df["reviews"]=all_reviews
    return place_df


def get_places(places_ll,cat_id):
    """Function to get all information about the places that have category id of (cat_id) for given coordinates(places_ll) 
    """
    place_df=pd.DataFrame()

    for l in places_ll:
        for n in cat_id:
            try:
                url = "https://api.foursquare.com/v3/places/search?limit=50"

                params = {

                    "ll": l,
                    "radius": "1500",
                    "sort": "RATING",
                    "categories": n,
                    "fields": "fsq_id,name,rating,geocodes,location,popularity,photos"
                
                }

                headers = {
                "Accept": "application/json",
                "Authorization": "Your API KEY"
                }
            
                place = requests.get(url,params=params ,headers=headers)
                cat_df = pd.json_normalize(place.json()["results"])
                place_df=pd.concat([cat_df,place_df])
                place_df=place_df.reset_index()
                place_df.drop("index",axis=1,inplace=True)
            except:
                pass
    place_df.drop_duplicates(subset=["fsq_id"], inplace=True)
    return get_reviews(place_df)


def get_all(se,nw,cat_id):
    """ Function to get all information and reviews of an area given by 'se: south east', 'nw: north west' coordinates. with the category ID's of 'cat_id

    cat_id=list of str
    n=integer
    se=nn.nn, nn.nn
    nw=nn.nn, nn.nn
    """
    places_ll=find_coordinates (se,nw)
    return get_places(places_ll,cat_id)

