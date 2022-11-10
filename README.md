# ePIF Gravity Forms

Gravity forms, built into Genomics website (https://genomics.oicr.on.ca) is a
much better forms interface than Google or Microsoft forms and we would prefer
to use it instead. However, the tooling isn't quite there compared to Google
or Microsoft, so we'll have to build some software to handle it instead.

This project is a prototype to demonstrate:

1. Retrieval from the Gravity Forms API (pull)
2. A web service that can receive web hooks from Gravity forms (push)

## Gravity forms credential file

First, create a file in this directory called `.gravity`. Inside should be three
lines: consumer_key, consumer_secret, and baseurl, in any order.

```
consumer_key=banana
consumer_secret=alsobanana
baseurl=https://genomics.oicr.on.ca/wp-json/gf/v2
```

The baseurl should be `https://genomics.oicr.on.ca/wp-json/gf/v2`. You can create
authentication tokens for `consumer_key` and `consumer_secret` on
[this page](https://genomics.oicr.on.ca/wp-admin/admin.php?page=gf_settings&subview=gravityformswebapi).

## Installation

This has been tested on Python 3.9.

```
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

## Running tests

Inside the virtual environment, run:

```
python3 test.py
```

You should see all the tests run and PASS.

## Methods

By default for form entries, Gravity Forms returns a horrendous format that has every field
labeled only by field ID. You have to separately request the labels
and apply them yourself. (Naturally, you can't use admin labels on the forms to
make this slightly more friendly. They don't come through the API) So right now
I'm replacing the numeric labels with their freetext labels, which isn't ideal.
I think the field IDs actually stay static even if the labels change, so ideally
there would be a mapping of id->computational label. However that will take a
long time, and since the form's format may change, I'll wait until we have
something stabilized. Ideally I would also isolate those fields that contain
duplicated information and make them more friendly, for example the two fields
that ask the type of assay to be run. But again, this is just a proof of concept.

For a rough example how the following methods work together, see `test.py`.

### getsession(key,secret)

Returns a session primed with credentials to connect to Gravity forms.

* key = consumer_key from .gravity file
* secret = consumer_secret from .gravity file

### get_forms(session,baseurl)

Returns a JSON file that describes all the forms on this site. Use this to find
the `formid` (id) for the form needed for the next few commands.

* session = from getsession
* baseurl = from .gravity file

### get_form_entries(session,baseurl,formid)

Returns ALL entries for a specific form in JSON format. The keys have been replaced
with their labels.

* session = from getsession
* baseurl = from .gravity file
* formid = the id of the form (from get_forms)

### get_form_entries_created_since(session,baseurl,formid,since)

Returns all entries created since a certain date.

* session = from getsession
* baseurl = from .gravity file
* formid = the id of the form (from get_forms)
* since = a string date in the format "yyyy-mm-dd hh:mm:ss"

### get_form_entries_updated_since(session,baseurl,formid,since)

Returns all entries updated since a certain date.

* session = from getsession
* baseurl = from .gravity file
* formid = the id of the form (from get_forms)
* since = a string date in the format "yyyy-mm-dd hh:mm:ss"
