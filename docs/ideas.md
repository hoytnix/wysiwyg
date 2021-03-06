The Word
========



- [ ] Dev: Feed to check for updates to librarys' docs/changes.
- [ ] Feature: wp-import => web-import:
    + Search Engine (Spidey) => AI
    + Rebuild static or mostly-static web-pages.
    + Auto-contact owners with preposed improvements.
    + Seemlesly re-build existing apps.

Re-engineer "Spidey" to archive, index, and analyze various web-applications:
    + CMS
        + Blog
    + E-Commerce
    + BBS
        + Craigslist
        + Forum
        + Stackoverflow
    + Support
        + FAQ
        + Issues
        + CRM
        + SMM
    + Wiki

+ Websites should be able to be rebuilt at least visually through translating raw-HTML to data-fixtures that fit the Anavah engine. (Translation.)
+ Specific functionality can be built for the most-valuable applications. 
+ It should be important to notice the difference between Disqus, Craigslist, and Stackoverflow: although they are all _bulletin-board applications_, they all have distinct differences in interface...
+ A value-assesment of the website should be made, along with gathering contact information for the owners so the may be approached with an offer.
+ Engine filters should be in place to filter outi anything not Christ-like, spam, bad words, negative content, etc.
+ Static-websites are gold because they're translated at the most basic level, provide the most benefit (speed, cost), as well as the ability to update information from a modern UI.



AI EXAMPLE
----------

```
Black Wheel           <- Title: largest text, first.
"It's a black wheel." <- Description: quotes.
$29.95                <- Price: ([0] in ($,...)
(25 / 3)              <- Variable/unit-price: prob. comes after "Price"
```


+ Should be built from the ground-up to run on the AWS-platform.
+ The engine need not be assembled until HTML can finally be translated to-and-from fixtures.
+ The engine needs a useable, binary-compiled, indexable, file-system. (Spidey issue.)
    + In fact, go make issues for Spidey and fix them in this update! (Done.)
+ The engine should run on its own with only initial input, until a specifed parameter is met, probably disk-space or quantity.
+ Contact information should be gathered on a case-by-case basis from the action-UI: initiation _must_ be a manual action performed by a human.



Filters
-------

- [ ] Bad-words
- [ ] Countries
- [ ] Word-frequency
- [ ]   Articles
- [ ]   Links
- [ ]   Matches in index
- [ ]   Sub-domains

Filters as well as categorization of websites based on word occurences can be assembled from information already embedded into Spidey comments/program.



INTRINSIC VALUE
---------------

Can be estimated by taking compiled HTML size, calculating the product of the AWS-request-cost and number of requests; and comparing it to the customer's current pricing.

Customer's pricing can be found as follows:
- [ ] Compile a list of hosting providers and their hostnames
- [ ] Scrape their pricing tiers
- [ ] Check website owner's whois for host, and index its price.
- [ ] Since utility is multitudes less expensive, use the lowest-tier, so customers who are paying more than that will have the added drama of "Oh we can actually save you 5000% then."

Compile the index of websites and their values into a sortable table for telemarketing, by me.



SSL
---

+ DNS for a multi-site network like this should be tricky but is required anyways.
+ Offer a free-SSL option, with whatever extra-costs not up-charged.
    + Has to be a dedicated-IP.
+ Offer option of a dedicated IP for self-SSL.
    + May up-charge for the IP.
+ Provide a platform for users to purchase SSL/DNS-support without human interaction:
    + Ordering without humans leaves no error for mistakes, pre-preperation, presentation, etc. (Think Google.)
    + Walk them through variables which effect pricing, and/or allow us to prepare.
    + Intelligently use information compiled on their providers:
        + Scrape images, info, etc.
        + Depending on if they use mail or not, just chaging a name-server may not cut it: do your research!
+ Support fees will probably be a major financial source for the initial development:
    + Small-static websites may be drastically less-expensive on the Anavah platform,
        + however, their value is also correlated to that low traffic so we don't make much.
    + Live support will be a gateway to connecting with customers and building rapport;
    + Rapport will be used to offer upgrades, future proposals (like the release schedule price changes), etc.
+ It may be beneficial to partner with a provider such as Namecheap...
    + The LORD _will_ provide a list of providers to partner with financially.



SCHEDULE
--------

- [ ] 1. Pack an element-dict.
- [ ] 2. Unpack an element-dict.
- [ ] 3. Translate HTML to an element-dict.
- [ ] 4. Releate elements to data-representations.
- [ ] 5. Create an UI for interacting with element-structures.
- [ ] 6. Create an interactive guide/tutor for the UI.
- [ ] 7. Get Aaron on-board to test, so features and testing-framework may be proven.
- [ ] 8. Develop the search-engine.
- [ ] 9. Compile data to actionable customer-acquisition.
