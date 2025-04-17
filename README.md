# CS3028 Group Project

## Datasets for Objects and Models (D.O.M)

Welcome to your new program! Here's a quick guide to get started along with some tips and tricks to help you make the most of it.

---

### Introduction

Generating images of 3D objects can be tedious when working with large datasets. D.O.M. is here to simplify the process. This program is designed to help you efficiently generate datasets for your 3D objects. It aims to make dataset generation easier, while offering a dedicated tool for your needs.

---

### Getting Started

To run D.O.M., simply execute the `UI.py` file located in the `frontend` folder.

#### Steps:
1. Begin by loading a tutorial object or uploading an object.
   
   ![Import](https://github.com/user-attachments/assets/b0347dd6-a998-4835-8b02-1d7f74b0b523)
   
2. When uploading a custom object, you can choose to upload an individual file or a folder. (Uploaded items will share their file name within the software.)
   
   ![ImportObject](https://github.com/user-attachments/assets/9be4bc43-706f-49d1-bba7-b8a18c836b0a)

3. Once an object is uploaded, the viewport will automatically update. Any changes you make to elements in the scene will trigger automatic updates in the viewport.
   
   ![ViewPort](https://github.com/user-attachments/assets/f0d98f25-bd9e-460c-8dc0-ad9af0054891)

---

### Object Bar

When an object is uploaded, the **ObjectBar** will append an element. This allows you to specify whether particular objects in the scene should be grounded or not.

![ObjectBar](https://github.com/user-attachments/assets/231890b4-e054-4261-a474-8c23af543a05)

---

### Object Tab

The **ObjectTab** enables users to change the starting elements for each object. Users can select the object via the combobox (highlighted in orange below).

![Object](https://github.com/user-attachments/assets/72ea49f7-d8d8-4055-b372-562faa2bf6dd)

---

### Pivot Tab

The **PivotTab** allows users to:

- Specify a custom pivot point (red).
- Assign an object as the pivot point (blue).
- Set the distance between the camera and the pivot point in meters (green).

![Pivot](https://github.com/user-attachments/assets/be6fc5f3-f61f-4f1b-9b59-370c0bab6c49)

---

### Render Tab

The **RenderTab** provides options to configure rendering settings:

- Specify the number of renders to generate (red).
- Define the change in degrees per axis of freedom (green).
- Begin rendering by pressing **Generate Renders** (blue).
- Use the unlimited render feature to generate renders continuously until manually stopped (orange).

![Render](https://github.com/user-attachments/assets/f5223a4e-95d6-42d4-a7d6-d8453f2856ee)

- Preview the current render configuration before generating final outputs (pink).

![RenderPreview](https://github.com/user-attachments/assets/33590fe2-8747-425e-a48c-ed89d84268fd)

---

### Lighting Tab

The **LightingTab** lets users fine-tune lighting options:

- Adjust light strength (red).
- Change light color (green).
- Modify light radius (blue).
- Select the type of light (pink).
- Specify light position (orange).
- Set light angle (neon).

![Lighting](https://github.com/user-attachments/assets/bceebf17-a4ea-4607-99c6-cf523cc34593)

---

### Random Tab

The **RandomTab** allows fields across all pages to be set to random:

- Activate randomness globally (red).
- Set randomness per set (green) or per frame (blue).
- Adjust the random seed value (orange).

![RandomBase](https://github.com/user-attachments/assets/d1386ab1-8699-4d6d-b351-3e3f91c4211a)

#### Random Selection:

- Activate specific fields using the checkbox (red).
- Define lower and upper bounds for random elements (green and blue).
- Change the target object (orange).
- Set all elements on the current page to active (pink).

![RandomSelection](https://github.com/user-attachments/assets/31607e0a-3a9e-49d3-8168-c0cf4cac67fe)

---
### Citation and Terms of Use

1. Scope of License
As defined by https://creativecommons.org/share-your-work/cclicenses/

CC BY-NC-SA

This license enables reusers to distribute, remix, adapt, and build upon the material in any medium or format for noncommercial purposes only, and only so long as attribution is given to the creator. If you remix, adapt, or build upon the material, you must license the modified material under identical terms. CC BY-NC-SA.

2. Restrictions
- Users agree not to employ automated systems, algorithms, or processes—including but not limited to web crawlers, data scraping tools, or AI models—to extract or analyse any part of this software or its associated data.
- The software or its contents shall not be integrated into training datasets for machine learning or AI systems. The outputted data may be used in non-commercial AI training.
- Users agree not to attempt reverse engineering, decompiling, disassembling, or modifying any part of the software, unless the altered software is made available as open source

3. Attribution
Any research or publications resulting from the use of this software must include proper citation and acknowledgment as specified by the software provider.

 - Oliver Japp, Ilya Waywell, Dominic Brown, Ben Brown, Ethan Burke, Miller Dawson, and Sophie Bowie. Datasets and Object Modelling (D.O.M). Version 1.0, April 15, 2025. https://github.com/b3nb07/CS3028_Group_Project.

4. Acceptance
By downloading, installing, or using the software, users acknowledge that they have read, understood, and agreed to these terms of use.



