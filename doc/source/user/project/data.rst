Data
====
The data tab contains the data which defines at which points in q the reflectivity is calculated for each contrast.
Different datasets can be loaded into a project and assigned to contrasts as needed. The available datasets are shown
in the data list on the left, each dataset has the **Name**, **Data Range**, and **Simulation Range** properties. The
properties for a specific dataset can be view by clicking on the name of the dataset in the list. These properties can
also be modified in edit mode although **Data Range**, and **Simulation Range** can also be modified outside edit mode
to keep consistency with RasCAL-1.

.. image:: /images/data_tab.png
   :scale: 60
   :alt: Data tab in Project Window
   :align: center

The **Simulation** dataset is the default value to use when no data is present in a contrast. This dataset cannot be
deleted from the data list or renamed but the **Data Range**, and **Simulation Range** properties can be adjusted
if needed.

.. image:: /images/data_tab_simulation.png
   :scale: 60
   :alt: Data tab showing Simulation entry
   :align: center


Add and Remove Data
-------------------
To add a new dataset, in edit mode:

1. Click the |add| button at the top of the data list.
2. Select a data file with a supported format in the file dialog. The following file formats are supported:
    * Text file (.dat) - 3 or 4 column ASCII file with or without a single line header.
    * ISIS histogram (.asc) - for back compatibility with RasCAL-1.
    * Nexus file (.nxs) - which should contain data in a |NXdata| entry.
    * |ORSO_file| (.ort)
3. The data will be loaded and shown in the preview table. Modify the name, data range, and simulation range as needed.


.. image:: /images/data_tab_editing.png
   :scale: 60
   :alt: Data tab in Edit mode
   :align: center


To remove a dataset, in edit mode:

1. Select a dataset to remove in the data list.
2. Click the |delete| button.
3. The selected dataset will be removed from data list along with any reference to it.


.. |NXdata| raw:: html

   <a href="https://hdf5.gitlab-pages.esrf.fr/nexus/nxdata_axes/classes/base_classes/NXdata.html" target="_blank">NXdata</a>

.. |ORSO_file| raw:: html

   <a href="https://www.reflectometry.org/advanced_and_expert_level/file_format" target="_blank">ORSO data file</a>
