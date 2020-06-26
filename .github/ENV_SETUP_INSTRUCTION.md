# BridgeInTech Development Setup Instructions 

Before you start, you need to have the following installed:
- [PostgreSQL database](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads)
- [pgAdmin4](https://www.pgadmin.org)

If you have these already installed, you are ready to start.

## 1st, Fork, Clone and Remote
1. Follow the instruction on the [Fork, Clone, and Remote](https://github.com/anitab-org/bridge-in-tech-backend/wiki/Fork,-Clone-&-Remote) page for this step.

## 2nd, Create a new virtual environment 

1. Create a new virtual environment: `virtualenv venv --python=python3`. Note: Do not use the same virtual environment for Mentorship System and BIT.
2. Activate the virtual environment: `source ./venv/bin/activate`

`source ./venv/bin/activate` may produce errors (no such directory errors) for Windows users who use Git Bash, because on Windows machines, virtual environments do not have the bin folder under venv. Instead, run the command `source ./venv/Scripts/activate`. This command only works on Git Bash on Windows machines. For Windows Command Line Users, run `.\env\Scripts\activate` instead. This command is for users running the program on Windows CMD.

Install all dependencies in the `requirements.txt` file: `pip install -r requirements.txt`

## 3rd, Create the main database

1. Run postgresql shell command: `psql`. 
2. Create database, name it "bit_schema": `create DATABASE bit_schema;`
3. If you are not currently connected as `postgres`, run the following to connect to the database you've just created as the superuser `postgres`.

// TO DO: SUPPLY IMAGE TO SHOW STEPS 1 AND 2 COMMAND LINES

4. Create the BIT schema: `create schema bitschema;`
5. Confirm to check the new schema has been added. 

You should see 2 schemas, public and bitschema.

// TO DO: SUPPLY IMAGE TO SHOW STEPS 5 IS CONFIRMED

You can now closed the psql shell by typing `\q` and hit `enter`.

## 4th, Open **pgAdmin4**

* ### Set local_data permissions
You should see the local_data and when you expand the arrow, you should see the 2 schemas.

<img width="154" alt="Screen Shot 2020-06-14 at 9 55 03 pm" src="https://user-images.githubusercontent.com/29667122/84592555-e2f9dd80-ae89-11ea-91b7-322605111961.png">


By default, `public` schema will be accessible to `PUBLIC` and `postgres` users. We need to make sure `bitschema` and `bit_schema` also have the same permission settings.
To do this, click on `bit_schema` on the left sidebar, go to `Properties` (top navbar) > `Edit` (top right) and adjust the settings under the `Security` tab to look like the screenshots below. Do the same with `bitschema`.

<img width="620" alt="Screen Shot 2020-05-07 at 7 47 39 pm" src="https://user-images.githubusercontent.com/29667122/81332957-2f156d80-90e7-11ea-9e15-53a607542388.png">


Note: If you happened to create the `bit_schema` under your username instead of `postgres`, don't worry, don't change anything else, just add `PUBLIC` access on top of the existing one.

* ### Create and set local_data_test
To set up the test database, do the same steps as creating `bit_schema` above (see `3rd` step), but change the name to `bit_schema_test` instead. Don't forget to also create `bitschema` as well as [2 other required schemas for PostgreSQL tests](https://github.com/sqlalchemy/sqlalchemy/blob/master/README.unittests.rst): **test_schema** and **test_schema_2**. Remember to change the permission settings to include `PUBLIC` in all added schemas.
Your **bit_schema_test** database should look like this screenshot now.

<img width="171" alt="Screen Shot 2020-06-14 at 9 57 41 pm" src="https://user-images.githubusercontent.com/29667122/84592600-2eac8700-ae8a-11ea-9035-c449068bdd7a.png">

Now we are ready to create the tables using Flask-Migrate.

## 5th, Set up migration script
1. Go to your project folder and look for the `migrations` folder. 
<img width="271" alt="Screen Shot 2020-06-14 at 10 01 05 pm" src="https://user-images.githubusercontent.com/29667122/84592646-92cf4b00-ae8a-11ea-9e17-4748c7c09182.png">

2. Copy and paste the folder (and its content) to the desktop.
3. Delete the original folder inside your project directory.
4. Run: `flask db init`. This should create a new `migrations` folder inside your project directory.
5. Replace the files in the newly created folder called `alembic.ini`, `env.py`, and `script.py.mako` with the same files from inside the `migrations` folder you placed on your desktop before.
6. Run: `flask db migrate -m 'initial migration'`. This will create an Alembic migration script under `versions` folder.
7. Open the migration script that newly created as well as the same file that has `......initial_migration.py` from the desktop `migrations` folder.
8. Except on the version informations, make the following changes to the new migration script inside the project folder:
  - copy paste lines 11 from the old file (on desktop) and replace the same sections on the new one.
<img width="543" alt="Screen Shot 2020-06-14 at 10 07 28 pm" src="https://user-images.githubusercontent.com/29667122/84592795-8b5c7180-ae8b-11ea-8d45-24a171816603.png">

   - change schema names (both on upgrade and downgrade). The auto-generated file will have 'bitschema' on all tables. Change to `public` on the relevant tables (for example, the `tasks-list` should have `public` as schema name)
The following tables belong to MS `public` schema: `users, mentorship_relations, tasks_list, tasks_comments`. Whereas `organizations, programs, personal_backgrounds, mentorship_relations_extension` belong to BIT `bitschema`.
 
<img width="663" alt="Screen Shot 2020-05-07 at 9 28 24 pm" src="https://user-images.githubusercontent.com/29667122/81350596-9b06ce80-9105-11ea-8a42-340c0bbf02f5.png">
<img width="570" alt="Screen Shot 2020-06-14 at 10 11 17 pm" src="https://user-images.githubusercontent.com/29667122/84592874-176e9900-ae8c-11ea-8985-321be0b6db3c.png">


   - Make sure you see the correct schema name at the front of each foreign key references. So **public.** should be the schema name for `ForeignKeyConstraints` within tables of `public` schema and **bitschema** should be the schema name for tables on `bitschema` side.
(for example, in `users_extension` table, instead of [users.id] you should have [public.users.id]
<img width="540" alt="Screen Shot 2020-06-14 at 10 16 00 pm" src="https://user-images.githubusercontent.com/29667122/84593006-ec387980-ae8c-11ea-954a-958e17b50a5e.png">


   - remove path reference on custom data type (JsonCustomType) inside `tasks_list` (the images shown what it should look like):
<img width="568" alt="Screen Shot 2020-05-07 at 9 35 46 pm" src="https://user-images.githubusercontent.com/29667122/81350784-15375300-9106-11ea-929c-c4c51009a4e0.png">

9. Do final check by comparing the old file vs new file of migration scripts.
10. Once done, run: `flask db upgrade`. This will create the tables inside your database.

<img width="226" alt="Screen Shot 2020-06-14 at 10 22 25 pm" src="https://user-images.githubusercontent.com/29667122/84593110-987a6000-ae8d-11ea-9f68-bed06ed736c0.png">

Note: The steps above are only for creating the `bit_schema` tables, not the `bit_schema_test`. The `bit_schema_test` tables will be automatically created, populated and dropped as part of the db test lifecycle when running the test cases.


That's it. Happy hacking 👌


