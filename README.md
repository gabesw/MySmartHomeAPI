# MySmartHomeAPI
REST API with Django REST to manage parts of my smart home and set up virtual switches

## Contents
- [About](#about)
- [Hurdles](#hurdles)
- [Example Automations](#example-automations)

## About
I started this project because I began to integrate smart home products with my home using the Apple Home system, and found some critical limitations of Apple's automation. One example of this is the creation of 'phantom' switches. e.g. a switch that is not attached to a physical Apple Home compatible device. It is really more of a global variable, but I wanted a feature that would enable me to modify the behaviour of my automations based on some button I press. I implemented this for my kitchen lights, which are controlled by an Aqara FP2 presence sensor. I often sit in my dining room to work which is on the border of the 'kitchen' zone in the Aqara app, so the lights would often randomly turn on or off when I didnt want them to. I realized that in the limited set of actions that an Apple Home shortcut can access, making HTTP requests to a url is included. Thus, I had the idea to use a REST API to implement a feature which would allow me to set this 'phantom' switch to 'stay-on', 'stay-off' or 'normal-behaviour' to change the behaviour of my kitchen light automation. Details of this can be found in [Example Automations](#kitchen-light-behaviour). My API is now running publically at [MySmartHomeAPI](https://mysmarthomeapi.software/) and is being hosted on a load-balanced AWS Elastic Beanstalk instance.

## Hurdles
### SSL and HTTPS
In the initial set-up of this project. I was using the provided AWS Elastic Beanstalk URL as I did not want to pay for a domain name. I realized I would need to have an SSL certificate for my API as I did not want to send tokens (or any data for that matter) over HTTP. Unfortunately, I realized that you cannot attach a signed SSL certificate to the provided Elastic Beanstalk URL because I do not have control over the DNS records, so I initially just created a self signed X509 certificate which produces an 'unsecure website' warning when accessed on the front end. I figured this would not be a problem as this is primarily a backend application. What I did not consider is that in the Apple Shortcuts or Home app, HTTP requests over HTTPS *must* be authenticated by a signed CA certificate. So I begrudgingly purchased a domain name and used [SSL For Free](https://www.sslforfree.com/) to get a trusted CA certificate and authenticated it using CNAME records. I then had to use AWS Route 53 to redirect requests from my domain to the Elastic Beanstalk instance using AWS's built-in Elastic Beanstalk alias records and changed the name servers on my domain name registrar to the Route 53 name servers. I finally now had secure requests over HTTPS that Apple shortcuts liked.

### Dynamic Endpoint Creation
While working on some new 'global variable' endpoints for the API (a simple endpoint with only two states: 0 and 1), I realized that there was a lot of repetitive code when creating a new global variable, having to add a new ViewSet, a new Model, a new Serializer, and add the endpoint to the router in urls.py. I then had the idea to implement a simple, modular way to create new global variable endpoints. There is a dictionary at the top of the global_var.py file and every entry added to the dictionary (a string -> 5-tuple mapping) will create a fully functioning API endpoint with its own Model, Serializer, ViewSet, auto-generated documentation, and front-end page in a single line of code! The file provides a single method which is to be called from urls.py with the url router as an argument. The function creates everything required for each of the endpoints and then registers the endpoints in the router. Then, when the router urls are added to urlpatterns, all of the auto-generated endpoints will be included. This can easily be extended to support endpoints of a common type other than global variable with very little additional code.

<br />
<br />
<br />
<br />

# Example Automations
## Kitchen Light Behaviour
This is the feature described in the [About Section](#about).
### Front-End Shortcut
Below is the Apple Shortcut I created to control the behaviour of my kitchen lights. This shortcut runs locally on each front-end device and *not* as a Home Automation. This enabled me to add the shortcut like an app on my homescreen:
![Kitchen light shortcut on my home screen](Examples/KitchenLightBehaviorApp.jpg?raw=true "Kitchen Light Behavior 'App'")
When the shortcut is run, this menu appears:
![Kitchen light shortcut menu](Examples/KitchenLightBehaviorAppInUse.jpg?raw=true "Kitchen Light Behavior Menu")
Selecting each menu item sends a PUT request to the [api/v1/kitchen/lights/keep_on/](https://mysmarthome.software/api/v1/kitchen/lights/keep_on/) endpoint of my API with the respective value for each option. This operation can be seen below in the 'code' for the shortcut:

![Kitchen light shortcut code](Examples/KitchenLightBehavior.jpg?raw=true "Kitchen Light Behavior Code")

### Back-End Automations
In the backend side of this feature, I make GET requests to [api/v1/kitchen/lights/keep_on/](https://mysmarthome.software/api/v1/kitchen/lights/keep_on/) to get the state of the behaviour switch. Using this value I can tell the automations that control turning on and off my kitchen lights to change their behavior based on the value returned by my API. Below are the shortcuts that are triggered by my FP2 sensor. First, the "presence in kitchen" automation:
![Presence in the kitchen shortcut](Examples/PresenceInKitchen.jpg?raw=true "Presence in Kitchen Shortcut")
And the "no presence in kitchen" automation:
![No presence in the kitchen shortcut](Examples/NoPresenceInKitchen.jpg?raw=true "No Presence in Kitchen Shortcut")

## More Examples Coming Soon!
