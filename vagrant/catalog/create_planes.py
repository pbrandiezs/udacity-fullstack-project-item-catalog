#!/usr/bin/env python

#
# create_planes.py
#
# This program populates the ItemCatalog database with several planes for testing.
#

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, ItemCatalog

#Connect to Database and create database session
engine = create_engine('sqlite:///ItemCatalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

#Add users
NewUser = User(email="pbrandiezs@gmail.com",
     id=1,
     picture="https://platform-lookaside.fbsbx.com/platform/profilepic/?asid=2296167867307191&height=200&width=200&ext=1559163571&hash=AeTcZcYDm6Y6E-zk",
     username="Perry Brandiezs"
)
try:
    session.add(NewUser)
    session.commit()
    print "User %s added" % NewUser.username
except:
    print "Not added - User %s" % NewUser.username
    session.rollback()

NewUser = User(email="mickeymouse@disney.com",
    id=2,
    picture="https://upload.wikimedia.org/wikipedia/en/thumb/d/d4/Mickey_Mouse.png/220px-Mickey_Mouse.png",
    username="Mickey Mouse"
)
try:
    session.add(NewUser)
    session.commit()
    print "User %s added" % NewUser.username
except:
    print "Not added - User %s" % NewUser.username
    session.rollback()

# Add planes
NewPlane = ItemCatalog(
    category_name="Gulfstream",
    item_name="G650ER",
    item_description="Long range private jet",
    user_id=1
)
try:
    session.add(NewPlane)
    session.commit()
    print "Plane %s added" % NewPlane.item_name
except:
    print "Not added - Plane %s" % NewPlane.item_name
    session.rollback()

NewPlane = ItemCatalog(
    category_name="Gulfstream",
    item_name="G550",
    item_description="A very nice jet",
    user_id=1
)
try:
    session.add(NewPlane)
    session.commit()
    print "Plane %s added" % NewPlane.item_name
except:
    print "Not added - Plane %s" % NewPlane.item_name
    session.rollback()

NewPlane = ItemCatalog(
    category_name="Gulfstream",
    item_name="G650ER",
    item_description="Mickey Mouse's Long range private jet",
    user_id=2
)
try:
    session.add(NewPlane)
    session.commit()
    print "Plane %s added" % NewPlane.item_name
except:
    print "Not added - Plane %s" % NewPlane.item_name
    session.rollback()

NewPlane = ItemCatalog(
    category_name="Crop Duster",
    item_name="Piper Cub",
    item_description="Little yellow airplane that spews toxic chemicals on the food supply to kill beneficial insects.",
    user_id=1
)
try:
    session.add(NewPlane)
    session.commit()
    print "Plane %s added" % NewPlane.item_name
except:
    print "Not added - Plane %s" % NewPlane.item_name
    session.rollback()

NewPlane = ItemCatalog(
    category_name="Falcon",
    item_name="10X",
    item_description="The Dassault Mystere/Falcon 10 is an early corporate jet aircraft developed by French aircraft manufacturer Dassault Aviation.",
    user_id=1
)
try:
    session.add(NewPlane)
    session.commit()
    print "Plane %s added" % NewPlane.item_name
except:
    print "Not added - Plane %s" % NewPlane.item_name
    session.rollback()

NewPlane = ItemCatalog(
    category_name="Embraer",
    item_name="Phenom 100",
    item_description="The Embraer EMB-500 Phenom 100 is a very light jet developed by Brazilian aircraft manufacturer Embraer.",
    user_id=1
)
try:
    session.add(NewPlane)
    session.commit()
    print "Plane %s added" % NewPlane.item_name
except:
    print "Not added - Plane %s" % NewPlane.item_name
    session.rollback()

NewPlane = ItemCatalog(
    category_name="Aerospatiale/BAC",
    item_name="Concorde",
    item_description="The Aerospatiale/BAC Concorde is a French-British turbojet-powered supersonic passenger airliner that was operated from 1976 until 2003. It had a maximum speed over twice the speed of sound at Mach 2.04 (1,354 mph or 2,180 km/h at cruise altitude), with seating for 92 to 128 passengers.",
    user_id=1
)
try:
    session.add(NewPlane)
    session.commit()
    print "Plane %s added" % NewPlane.item_name
except:
    print "Not added - Plane %s" % NewPlane.item_name
    session.rollback()