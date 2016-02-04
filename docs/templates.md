Templates
=========



Expressions
-----------

"Template components" are represented by expressions which map data to HTML.

+ Expressing HTML:
    + Can have custom attributes. 
        + {'class': 'custom-p'}
        + {'id': 'header'}
    + Can have multiple data-sources, AND HTML tags.
        + Like Python format.
        + '{} has made {} posts.' % (user_name, posts_total)
        + 'You have {} currency.' % currency_total

