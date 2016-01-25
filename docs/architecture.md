Database Management
-------------------

Secure, decoupled, unopinionated, cross-namespace, persistent-storage. 

_Namespace_: Controller


* Controller performs on the RDBMS, which populates the Redis (cached) store.

* User-applications only have access to the store (read-only).

* Applications only have access to their own namespace's store; 
    requests for data-modifications must be performed through redirecting to 
    the respective app.





Templates / HTML
----------------

Just-in-time HTML compiling for super-fast content-distribution.

_Namespace_: Controller


* Multi-level template inheritance.

* All HTML is compiled to static-form before being served.





Extension API
-------------

Enable the user to customize their experience with trusted third-party APIs.

_Namespace_: Controller


* Extensions are user-configured through UCP.

* API should have a URI-like-interface for interacting with various extensions.

```
    mail:      -> SendGrid (or) MailChimp (or) Emma
    pay:       -> Braintree (or) Stripe (or) Stellar
    analytics: -> GA (or) Clicky (or) Heap
```





Task-Queue
----------

Event-driven architecture model.

_Namespace_: Controller


+ No need for thousands of WGSI applications with their own ports;
    + The controller manages the rendering for all the requests in a restful way.






