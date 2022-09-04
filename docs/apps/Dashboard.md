# Brief Intro 
a simple dashboard application similar to Django Admin.

`operator` register new customers, check in existing customers using the mobile app.
`manager/operator/admin` manage operation data, such as customer information, operator information, etc. using the dashboard   

# Dashboard Demo Features
- Login required
- Display Different content and function for different type of user:
> 1. superuser
> 2. admin
> 3. store_manager
> 4. operator
> 
## apps in this Demo
- api: RESTful API to work with the [mobile app](https://github.com/954gmo/ReactNative_Mobile_App) 
- sites: manage customer information, view customer activities, manage operator, view operator activities
- accounts: Operators

## Functions and Features
`search/export` customer information, operator information (all, selected)

`send message w/o image(s)` to customers ( a single customer, selected customers, all customers)

`edit/disable` customer, operator

`modify` operator roles.
