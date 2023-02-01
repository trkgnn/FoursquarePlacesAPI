# Foursquare Places API usage

This code will let you pick a rectangular coordinate and get information about the cafes inside the coordinates. You can even change the category IDs based on [FSQ IDs](https://location.foursquare.com/places/docs/categories) 

## Why need this code?

FSQ API lets you get 50 places in each request call. By using this code you will make the request call with a radius of 1.5km for every coordinate thats pointed approx 2km away from each other in the rectangular area you provide. Which will return you a much bigger and efficient dataset.


## Documentation and Parameters for FSQ API

[Documentation](https://location.foursquare.com/developer/reference/place-search) 