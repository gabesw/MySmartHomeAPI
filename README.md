# MySmartHomeAPI
REST API with Django REST to manage parts of my smart home and set up virtual switches

#### Contents
- [About](#about)
- [Hurdles](#hurdles)
- [Example Automations](#example-automations)

## About
I started this project because I began to integrate smart home products with my home using the Apple Home system, and found some critical limitations of Apple's automation. One example of this is the creation of 'phantom' switches. e.g. a switch that is not attached to a physical Apple Home compatible device. It is really more of a global variable, but I wanted a feature that would enable me to modify the behaviour of my automations based on some button I press. I implemented this for my kitchen lights, which are controlled by an Aquara FP2 presence sensor. I often sit in my dining room to work which is on the border of the 'kitchen' zone in the Aquara app, so the lights would often randomly turn on or off when I didnt want them to. I realized that in the limited set of actions that an Apple Home shortcut can access, making HTTP requests to a url is included. Thus, I had the idea to use a REST API to implement a feature which would allow me to set this 'phantom' switch to 'stay-on', 'stay-off' or 'normal-behaviour' to change the behaviour of my kitchen light automation. Details of this can be found in [Example Automations](#example-automations). My API is now running publically at [MySmartHomeAPI](https://mysmarthomeapi.software/) and is being hosted on a load-balanced AWS Elastic Beanstalk instance.

## Hurdles
### SSL and HTTPS
In the initial set-up of this project. I was using the provided AWS Elastic Beanstalk URL as I did not want to pay for a domain name. I realized I would need to have an SSL certificate for my API as I did not want to send tokens (or any data for that matter) over HTTP. Unfortunately, I realized that you cannot attach a signed SSL certificate to the provided Elastic Beanstalk URL because I do not have control over the DNS records, so I initially just created a self signed X509 certificate which produces an 'unsecure website' warning when accessed on the front end. I figured this would not be a problem as this is primarily a backend application. What I did not consider is that in the Apple Shortcuts or Home app, HTTP requests over HTTPS *must* be authenticated by a signed CA certificate. So I begrudgingly purchased a domain name and used [SSL For Free](https://www.sslforfree.com/) to get a trusted CA certificate and authenticated it using CNAME records. I then had to use AWS Route 53 to redirect requests from my domain to the Elastic Beanstalk instance using AWS's built-in Elastic Beanstalk alias records and changed the name servers on my domain name registrar to the Route 53 name servers. I finally now had secure requests over HTTPS that Apple shortcuts liked.

## Example Automations
TODO
