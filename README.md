# CS3028_Group_Project

Datasets for Objects and Models (D.O.M)
Welcome to your new program! Here is a quick guide to get started and a few tips and tricks to help you along.

Introduction

Generating images of your 3D objects can become a tedious task when generating large datasets, but DOM is here to help you. DOM is a simple program designed to help you generate your datasets in a much more efficient way. Aiming to help you gain more ease in dataset generation and allow you to use a dedicated program for your purpose



Contents:

Subject                                     Line
Introduction	                              6
Getting started	                            28
How to import Objects	                      42
How to delete an object	                    53
How to import Settings	                    68
How to export settings	                    81
How to manipulate an object	                94
How to set a pivot point	                  117
How to Render an image	                    140
How to generate random variable values	    159



Getting started

In order to run DOM, all you need to do is run the UI.py file in the frontend folder

To begin with you will see a pop-up box prompting you to either enter your custom object – or pick from our tutorial objects if you are just wanting to run a test through the program.

![alt text](images/image.png) 

The custom object option will allow you to browse through your own files to find the desired object. Picking tutorial objects will bring up the menu below showcasing our 6 tutorial objects to pick between

![alt text](images/image-1.png)
 
After selecting your object you will be able to view your object within our viewport, edit it as desired, then generate your dataset of renders


How to import Objects

DOM allows you to import in multiple objects for your scenes if desired. To do this simply make your way to the Import and Export tab

![alt text](images/image-2.png)
 
Once there simply press the “Import Object” button and you will be able to search through your files for the desired object
 
![alt text](images/image-3.png)


How to delete an object

You are also able to delete an object if desired. To do this simply make your way to the Import and Export tab

![alt text](images/image-4.png)
 
Select the “Delete Object” button

![alt text](images/image-5.png)
 
And then select the object you wish to delete from the given list

![alt text](images/image-6.png)


How to import Settings

If you have a specific set of setting you want to apply to your object in the form of a JSON file, you can upload it as follows: First go onto the Import and Export tab

![alt text](images/image-7.png)
 
Then select the “Import Settings” button

![alt text](images/image-8.png)
 
This will take you into your files to select your chosen JSON file and once uploaded will be applied to your objects


How to export settings

If you want to share your settings you are also about to export your settings as follows. First make your way into the Import and Export tab

![alt text](images/image-9.png)
 
Then select the “Export Settings” button

![alt text](images/image-10.png)
 
This will then generate a JSON file for your current settings and can be re applied to the program using Import Settings


How to manipulate an object

To manipulate an object, first ensure you are on the Object tab

![alt text](images/image-11.png)
 
You can then move the object around the space using the 3 co-ordinate buttons

![alt text](images/image-12.png)
 
You can scale certain aspects of your object using the 3 scale sliders

![alt text](images/image-13.png)
 
You can also rotate the object around its 3 axes independently using the 3 rotation sliders

![alt text](images/image-14.png)
 
Selecting this box will allow you to choose between all the objects you have placed to specify which object it is you are trying to manipulate

![alt text](images/image-15.png)
 

How to set a pivot point

To set a pivot point first make sure you are on the Pivot Point tab

![alt text](images/image-16.png)
 
Selecting this tickbox will allow you to set a custom pivot point at a co-ordinate of your choosing

![alt text](images/image-17.png)
 
Once ticked, simply set your coordinate using the buttons below

![alt text](images/image-18.png)
 
Otherwise, if you wish to have an object as the pivot point you can select one using the dropdown on the right 

![alt text](images/image-19.png)
 
Once a pivot has been chosen you can then select the distance from the pivot point the images will be selected from using the Distance slider

![alt text](images/image-20.png)
 

How to Render an image

To render an image first make sure you are on the Render Tab

![alt text](images/image-21.png)
 
Next select how many renders you would like to generate

![alt text](images/image-22.png)
 
You can then select if you would like any degree change between the renders and which axis you would like to change

![alt text](images/image-23.png)
 
Finally hit the Generate Renders button to generate your renders

![alt text](images/image-24.png)
 

How to generate random variable values

To generate random variable values first make sure you’re on the Generate Random Tab

![alt text](images/image-25.png)
 
You should first select which object you want to randomise using the drop down menu

![alt text](images/image-26.png)
 
Next you can either randomise all variables by selecting this check box

![alt text](images/image-27.png)
 
Or by selecting any checkbox you want to have randomised 

![alt text](images/image-28.png)
 
Your randomisation will generate a seed which will be displayed here
 
![alt text](images/image-29.png)