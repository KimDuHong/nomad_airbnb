# House Hosting Website

This project is a house hosting website inspired by Airbnb, designed to provide a seamless and efficient platform for users to book and manage their stays.

# My Personal Website

This is my personal website, where I showcase my work and provide information about myself.

## Table of Contents

- [Description](#description)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation and Setup](#installation-and-setup)
- [Contributing](#contributing)
- [Features Implemented](#features-implemented)

## Description

This website serves as a personal portfolio where I can showcase my work and provide information about myself. It contains sections for my bio, my projects, my skills, and my contact information.

## Features

- Home page with a brief introduction and links to other sections
- Projects page with information about my projects and links to their live demos and source code
- Skills page with a list of my technical skills and tools
- Contact page with a contact form for users to send me a message

## Technologies Used

- Django
- Django REST Framework
- daphne
- channels
- ...

## Installation and Setup

To install and run the project locally, follow these steps:

1. Clone the repository: 

git clone https://github.com/KimDuHong/nomad_airbnb


2. Navigate to the project directory: 

cd nomad_airbnb


3. Install dependencies: 

poetry init and poetry shell 


4. Start the development server: 

python manage.py runserver

5. Open the project in your web browser at `http://localhost:8000`

## Contributing

This is a personal project and contributions are not currently accepted. However, feedback and suggestions are always welcome.

# Features Implemented

## DB
-User
Extends Django's built-in AbstractUser model.
Has additional fields for name, is_host, avatar, gender, language, and currency.
-Category
Represents categories of listings, such as rooms or experiences.
Has a name and a kind field, which can be rooms or experiences.
-Amenity
Represents amenities that a room can have.
Has a name and description field.
-Room
Represents a listing for a room.
Has a name, country, city, price, number of rooms, number of toilets, description, address, pet-friendly status, kind, owner, and a category field.
Has a many-to-many relationship with Amenity through amenities field.
Has a one-to-many relationship with Photo through photos field.
Has a one-to-many relationship with Review through reviews field.
Has a many-to-many relationship with Wishlist through wishlists field.
-Photo
Represents a photo for a room.
Has a file and a description field.
Belongs to a Room through room field.
-Review
Represents a review from a User to a Room or Experience.
Has a user, a room, an experience, a payload, and a rating field.
-Experience
Represents a listing for an experience.
Has a country, city, name, host, price, address, start, end, description, and a category field.
Has a many-to-many relationship with Perk through perks field.
Has a one-to-one relationship with Video through video field.
Has a one-to-many relationship with Photo through photos field.
Has a one-to-many relationship with Review through reviews field.
Has a many-to-many relationship with Wishlist through wishlists field.
-Perk
Represents a perk that an experience can have.
Has a name, details, and explanation field.
-Video
Represents a video for an experience.
Has a file field.
Belongs to an Experience through experience field.
-Wishlist
Represents a wishlist created by a User.
Has a name and a user field.
Has a many-to-many relationship with Room through rooms field.
Has a many-to-many relationship with Experience through experiences field.
-Chatting_Room
Represents a chatting room created by users.
Has a name field.
Has a many-to-many relationship with User through users field.
Has a one-to-many relationship with Message through messages field.
-Message
Represents a message sent in a Chatting_Room.
Has a text, a sender, a room, a read status, and a sequence number field.
