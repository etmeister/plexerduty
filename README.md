plexerduty
==========

Small script to send pagerduty incidents as notifications to plex clients.  Designed to be run via cron.  Requires pygerduty.

usage
==========

1.  Generate PagerDuty API key via PagerDuty website.
2.  Create ~/.pygerrc file with at least pagerdutyApiKey and pagerdutyHost options.
3.  Create cron entry for plexerduty.py

options
==========
- cronInterval: Time in minutes to check for incidents.  Defaults to 30.
- plexApiUrl: Url for plex notifications. Defaults to "http://127.0.0.1:3005/jsonrpc".
- pagerdutyHost: Hostname for PagerDuty.
- pagerdutyApiKey: API Key for PagerDuty.
- notificationDelay: Seconds to wait between notifying for incidents.  Allows for readability.  Defaults to 5.
- triggeredOnly: Only show alerts for unacked/unresolved incidents.  Defaults to true.
