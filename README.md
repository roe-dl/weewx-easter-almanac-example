# weewx-easter-almanac-example
Example how to write an almanac extension for WeeWX

This is an example how to write an almanac extension for WeeWX. It provides the date of the easter sunday calculated by the formula of Carl Friedrich Gauß.
    
Put in your skin:
* `$almanac.easter.format('%Y-%m-%d')`
* `$almanac(almanac_time=time).easter.format('%Y-%m-%d')`

Replace the format string by the date format of your choice.
        
As this is an example, it is simple. One attribute is calculated only. A real world extension would provide a `next_easter` and `previous_easter` attribute as well. 
