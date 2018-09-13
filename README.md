# Password Reset Scheduler

## Setup

Create a MySQL instance with a database and set the root user password.

Execute the following command from the project directory, replacing `DATABASE` with your database name:

```bash
mysql -u root -p DATABASE < password_update.sql
```

Edit the `lp_update_sa.py` script with your database and LiquidPlanner information.

Edit the `passgen.sh` script with the PGP key fingerprints of all users who should have access to the passwords.

Create a cron job to run the scripts such as the following, including email addresses for all users who should receive passwords and notifications:

```bash
MAILTO=person1@cpcc.edu,person2@cpcc.edu
#
#
#

0 7 * * MON,TUE,WED,THU,FRI    username        cd /path/to/password-reset-scheduler/ && ./lp_update_sa.py
```

Replace the username above with the user of your choice. Ensure that user has imported all team members' PGP public keys into its keyring.

Add an entry to the `password_reset` table and set the `next_event` to a date in the next two weeks, then run `./lp_update_sa.py` and verify that it returns an account name and encrypted password.