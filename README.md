# Howl
A dead man's switch that sends alerts if a GET request doesn't arrive on time.
Check out [wolf](https://gitlab.com/huggles/wolf) for a cli client to help streamline the process of checkin.

## DISCLAIMER
*DO NOT USE HOWL TO PROTECT ANYTHING IMPORTANT*. Howl is extremely alpha
and should not be trusted. Howl comes with ABSOLUTELY NO WARRANTY. I am not
responsible for any damages.

## Services
A service is a platform which can send data like emails or discord. Currently
the supported services are:

 - Email

Adding a service only requires adding a class to `services.py`. Refer to
`Email` as a template.

## Checkin
The action of sending a GET request to Howl to notify it that you still exist.

## Alerts
An alert defines when and how to use one or more services. Alerts are
configured by yaml files which are stored in the `alerts` directory.
The name of the yaml file is the name of the directory. An example alert

```yaml
timeout: 48

services:
  - !Email
    recipient: example@example.com, example2@example.net
    sender: example@example.com
    subject: Ahh-wooooooo!
    body: |
      Hello World!

      <3 Howl

  - !Email
    recipient: example@example.com
    sender: example@example.com
    subject: Ahh-wooooooo!
    body: |
      Another email from the example alert.

      <3 Howl
```

So lets break it down:

- `timeout:` defines how the how long, in hours, to wait since the last check
in before the alert is triggered. If `timeout` is set to `None` then the alert
will only be able to be triggered manually.
- `services:` is a list of the services to use.
- `!Email` tells Howl what service to use, substituting `Email` with the service name. This is then followed by service
specific configuration.

## Deploying
Docker:

```sh
docker run -d \
  --name howl \
  --restart always \
  -p 5000:5000 \
  -v /srv/howl/:/howl/alerts/ \
  -e "USERNAME=test" \
  -e "TOTP_SECRET=base32secret3232" \
  registry.gitlab.com/huggles/howl
```

## Configuration
The main application environment variables
for configuration.

Environment Variable | Description | Default
--- | --- | ---
`LOG_LEVEL` | Set the log level. Possible values are DEBUG, INFO, WARNING, ERROR or CRITICAL. | `INFO`
`USERNAME` | Used in conjunction with `PASSWORD` to authenticate the user. | `NONE` but this must be set or you'll get ugly errors.
`TOTP_SECRET` | A base32 encoded string used to generate the totp password. | Randomly generated.
`CHECK_INTERVAL` | The amount of time in seconds to wait between checking if any alerts should be sounded. | 21600

## Email Service Configuration
The email service can be configured with the following environment variables.

Environment Variable | Description | Default
--- | --- | ---
`SMTP_HOST` | The url to a SMTP server to use for sending emails. | `None`
`SMTP_PORT` | The port of the SMTP server used to send emails. | `None`
`SMTP_USERNAME` | The username of the SMTP server. | `None`
`SMTP_PASSWORD` | The password of the SMTP server. | `None`

## Building
Same as every other docker image:

```sh
docker build -t howl .
```

## Contribute
Go for it!

## Licence
Deposer is distributed under the GNU General Public License Version 3.
