# jumpingminds-task

## 1. Post Request to create Elevator System with n elevators
<img width="1015" alt="image" src="https://github.com/ClawedCatalyst/jumpingminds-task/assets/97229491/c9c9043b-bb12-4545-9c51-5d7e53552a88">

## 2. Post Request to create Elevator Request to get the optimal Elevator
<img width="1008" alt="image" src="https://github.com/ClawedCatalyst/jumpingminds-task/assets/97229491/f29ac132-afc3-408b-9701-60aebde2f1ed">

## 3. Get request to get the elevator direction
<img width="1016" alt="image" src="https://github.com/ClawedCatalyst/jumpingminds-task/assets/97229491/2ee93a97-b804-4a24-b885-c138182c977c">

#### Error if elevator id does not exists
<img width="1021" alt="image" src="https://github.com/ClawedCatalyst/jumpingminds-task/assets/97229491/1fe33e60-e130-48e0-8c5b-65e6df0e2215">

## 4. Get elevator requests for a given elevator
<img width="1023" alt="image" src="https://github.com/ClawedCatalyst/jumpingminds-task/assets/97229491/85605b74-49d5-40ad-87e1-d8e8cf9e67bd">

## 5. Get next destination floor for the given elevator
<img width="1030" alt="image" src="https://github.com/ClawedCatalyst/jumpingminds-task/assets/97229491/5d012912-adfa-4c48-87bf-fa867b677aa4">

## 6. Move Elevators by one floor
<img width="1018" alt="image" src="https://github.com/ClawedCatalyst/jumpingminds-task/assets/97229491/db7c43ec-5670-4715-b55d-46023c4d760a">

## 7. Mark Maintainance.
<img width="1021" alt="image" src="https://github.com/ClawedCatalyst/jumpingminds-task/assets/97229491/f2e14d47-f548-4091-9038-0b92cbc7a3f9">

## 8. Patch request to open and close door.
<img width="1022" alt="image" src="https://github.com/ClawedCatalyst/jumpingminds-task/assets/97229491/99c5dd0d-09c7-4832-9a00-1511df3932fb">

#### Error if a user request to open the door if an elevator is busy.
<img width="1017" alt="image" src="https://github.com/ClawedCatalyst/jumpingminds-task/assets/97229491/89b323b0-a78e-4326-8350-2350d454712b">

#### Error if a user request to open the door if an elevator which is under maintenance
<img width="1020" alt="image" src="https://github.com/ClawedCatalyst/jumpingminds-task/assets/97229491/0120948e-26b7-475a-b185-917698e20ebf">

# Elevator System Documentation

## Request Status Definitions

### 1. In Process
- **Description:** The user has requested the elevator, and the elevator is currently in the process of reaching the user.

### 2. In Service
- **Description:** Indicates that the user is currently inside the elevator, and the elevator is actively providing its service.

### 3. Done
- **Description:** Signifies that the elevator has successfully completed its task of transporting the user to the desired floor.

<div style="display: flex; flex-wrap: wrap; justify-content: space-between;">
    <div style="flex: 1; margin-right: 5px;">
        <img width="300" alt="image" src="https://github.com/ClawedCatalyst/jumpingminds-task/assets/97229491/0738f752-b8b6-4a76-b27c-6d65d9ac3da2">
        <img width="300" alt="image" src="https://github.com/ClawedCatalyst/jumpingminds-task/assets/97229491/6006d013-d5b1-49cf-b14a-23e14ca6d833">
    </div>
 <div style="flex: 1; margin-left: 5px;">
        <img width="300" alt="image" src="https://github.com/ClawedCatalyst/jumpingminds-task/assets/97229491/b083ded7-8e1d-4258-b047-d94f7db4227e">
        <img width="300" alt="image" src="https://github.com/ClawedCatalyst/jumpingminds-task/assets/97229491/9faf5ca8-a3d6-4dbc-bb36-8773ef7f4fca">
    </div>
  <div style="flex: 1; margin-left: 5px;">
        <img width="300" alt="image" src="https://github.com/ClawedCatalyst/jumpingminds-task/assets/97229491/caddd771-04a4-4a5e-a117-7be0cdab33a2">
        <img width="300" alt="image" src="https://github.com/ClawedCatalyst/jumpingminds-task/assets/97229491/5392cde6-05e5-477b-959a-217b6a5d0d75">
    </div>
</div>


## Elevator Request 
To optimize elevator requests, a comparison is made between two potential elevators: one marked as "free" and the other as "busy." Prior to making a request, a condition check is implemented to assess the efficiency of each elevator. The system assigns the optimal elevator to the request by evaluating factors such as availability and processing time, ensuring that the chosen elevator is the most suitable for the given conditions.

## Database Design 

# SETUP

1. Clone the repository:

```CMD
git clone https://github.com/ClawedCatalyst/jumpingminds-task.git
```

To run the server, you need to have Python installed on your machine. If you don't have it installed, you can follow the instructions [here](https://www.geeksforgeeks.org/download-and-install-python-3-latest-version/) to install it.

2. Install, Create and activate a virtual environment:

```CMD
pip install virtualenv
virtualenv venv
```

Activate the virtual environment

```CMD
source venv/bin/activate
```

3. Install the dependencies:

```CMD
pip install -r requirements.txt
```

5.Run the migrate command

```CMD
python manage.py migrate
```

6. Run the backend server on localhost:

```CMD
python manage.py runserver
```

You can access the endpoints from your web browser following this url

```url
http://127.0.0.1:8000
```

7. You can create a superuser executing the following commands

```CMD
python manage.py createsuperuer
```

A prompt will appear asking for username followed by password.
To access the django admin panel follow this link and login through superuser credentials

```url
http://127.0.0.1:8000/admin/
```

## Hosted LINK - 
https://jumpingmind-task.suhaila.tech/







