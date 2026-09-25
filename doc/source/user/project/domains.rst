Domains
=======
A domains calculations relies on grouping the layers into domains, then grouping the defined domains into contrasts,
according to a domain ratio parameter. A domain ratio can be defined in the domains tab then referenced in a contrast.
For a standard layers project, the domains or domain contrast can also be created in the domains tab and referenced in
the contrast, Custom Layer and Custom XY projects are expected to group the domains in their associated custom
functions.

The domains tab will only be visible when the **Calculation** is set to **domains**. It contains a parameter table for
domain ratios .

.. image:: /images/domains_tab_custom_project.png
   :scale: 60
   :alt: Domains tab for Non-standard Layers Project
   :align: center


It also contains a table for domain contrasts if the **Model Type** is standard layers. Each row in the domain contrast
table has the following properties:

* **Name**: The name of the domain contrast.
* **Model**: This is should be layer or list of layer names that make up the slab model for the domain contrast.


.. image:: /images/domains_tab_standard_project.png
   :scale: 60
   :alt: Domains tab for Non-standard Layers Project
   :align: center

Add and Remove Domain Ratios
----------------------------
To add a new domain ratio (in edit mode):

.. image:: /images/domains_ratio_editing.png
  :scale: 60
  :alt: Domains Ratio table in Edit mode
  :align: center

1. Click the **Add new Domain Ratio** button at the top right of the tab.
2. A new row entry will be added to the table with an auto generated name. The name can be changed by double clicking
   the cell.
3. Modify the other entries by double clicking the cell and select the appropriate value from the dropdown.

To remove a domain ratio (in edit mode), simply click the |delete| button on the specific row you want to remove.

Add and Remove Domain Contrasts
-------------------------------
To add a new domain contrast (in edit mode):

.. image:: /images/domains_contrast_editing.png
  :scale: 60
  :alt: Domains Contrast table in Edit mode
  :align: center

1. Click the **Add new Domain Contrast** button at the top right of the **Domain Contrast** table.
2. A new row entry will be added to the table with an auto generated name. The name can be changed by double clicking
   the cell.
3. Modify the model by double clicking the cell, click the |add| button, and select a layer from the dropdown.
   Repeat and select as many layers as needed. A layer can be removed from the model by clicking the layer name and
   clicking the |delete| button in the model cell.

   .. image:: /images/adding_layer_to_domain_contrast.png
     :scale: 60
     :alt: Adding Layer to Domains Contrast
     :align: center

To remove a domain contrast (in edit mode), simply click the |delete| button on the specific row you want to remove.
