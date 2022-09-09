# Sunday Engineering Coding Challenge
### The purpose of this exercise is for you to demonstrate your ability to:
1. Understand requirements and translate those requirements into code
2. Demonstrate your ability to contribute to an existing codebase
3. Give us a working code sample to discuss

### This exercise is not intended to
1. Be perfect
2. Take more than 2-4 hours

## Instructions
This repo is a WIP and already contains the beginnings of a rudimentary order management system.

Your task is to add a `shipments` app satisfying the following criteria:
1. At the moment, an `Order` contains 5-12 `Products` and our goal is to deliver these products on **three, evenly spaced** shipment dates.
2. Each `Product` weighs one or two lbs, and each individual shipment can not total more than 5lbs.
3. To whatever extent possible, duplicate `Products` should be sent on different shipment dates.
4. Shipments must take place between April 1st and October 1st, and should occur in the same calendar year if the order was placed during the shipment window.

Functionally this will roughly be
1. Some process that creates `Shipments` from `Orders`
2. An endpoint to get information about shipments

## General Guidelines
Feel free to make any modifications/updates to the existing codebase to support your architectural vision.
Tests have been purposefully omitted, but we expect you to write some... in the framework/style of your choosing.
