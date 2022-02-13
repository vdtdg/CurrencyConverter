# CurrencyConverter

Simple API to convert amount of currencies with almost real-time data.

Taking advantage of a free API that have a low monthly-request pool, we still manage to build a service for ourselves
that is able to convert currencies at the rate we want.

Developed in TDD fashion, very robust.

## Usage

It's a standard Flask app.

You need first to setup a proper Python environment

```bash
pip install -r requirements.txt
```

Then start the Flask server:

```bash
export FLASK_ENV=app 
flask run
```

The exposed port of this service is 5000.

You can then use the /convert with a POST http request to get data.

### Example

POST to /convert with body

```json
{
  "currency": "USD",
  "amount": 13.4,
  "target_currency": "EUR"
}
```

Will answer :

```json
{
  "timestamp": "132651914911",
  "currency": "USD",
  "amount": 13.4,
  "target_currency": "EUR",
  "target_amount": 11.2
}
```