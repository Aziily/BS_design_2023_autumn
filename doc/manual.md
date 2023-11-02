# Manual

## 0 Menu

There pages(views) in the project can be listed below

- Login
- Dashboard
- Map
- Device
  - Add
  - Edit
  - Sensor
  - Actuator
- Message
- User
  - List
  - Add
  - Edit



## 1 Login

This is the page for logining with a existed user. Just enter the `username` in first line and `password` in the second line, then login to use the panel.

> By default, there are some user
>
> - Admin Privilege User
>   - `username`: admin
>   - `password`: admin123
> - Normal User
>   - `username`: user
>   - `username`: user123

<img src="./imgs/%E6%88%AA%E5%B1%8F2023-11-02%2010.04.31.png" alt="截屏2023-11-02 10.04.31" style="zoom:50%;" />



## 02 Dashboard

> Left side is the bar for menu, which is the same for all pages

There are four main part in the dashboard.

- **User information**: The part on the left top, showing the user information
- **Technology icon**: The part on the left bottom, which are the icons of the technology used in the project
- **Device Summary**: The part on the right top, showing the online devices with total devices and the data packages
- **Device kind**: The part on the right bottom, showing the detail of the information above

Also there is a github icon on the right top corner, jumping to the project page

<img src="./imgs/%E6%88%AA%E5%B1%8F2023-11-02%2010.11.44.png" alt="截屏2023-11-02 10.11.44" style="zoom:50%;" />



## 03 Map

The page shows all devices location on the map. There is detailed information when hover one map nail.

<img src="./imgs/%E6%88%AA%E5%B1%8F2023-11-02%2010.18.10.png" alt="截屏2023-11-02 10.18.10" style="zoom:50%;" />



## 04 Device

### Add

Enter by path `Device/{sensor or actuator}` and click button add, or just use path `device/add`. Enter the information about the new device and click add then there will be a new device. The map is used for choosing location by click the location on map.

> `*`items means items must be entered.

<img src="./imgs/%E6%88%AA%E5%B1%8F2023-11-02%2010.19.55.png" alt="截屏2023-11-02 10.19.55" style="zoom:50%;" />

### Edit

Enter by `Device/{sensor or actuator}` and click the edit icon

Like the add page, but there are information from the origin. After edition, click edit to submit

<img src="./imgs/%E6%88%AA%E5%B1%8F2023-11-02%2010.23.33.png" alt="截屏2023-11-02 10.23.33" style="zoom:50%;" />

### Sensor

Sensor devices page, one add button and cards of each device.

There are some important information about the devices, description need click to show.

There are three buttons with each card:

- **Edit**: for entering the edit page with selected device
- **Delete**: delete the selected device
- **Full**: show the detailed information about the device

<img src="./imgs/%E6%88%AA%E5%B1%8F2023-11-02%2010.26.24.png" alt="截屏2023-11-02 10.26.24" style="zoom:50%;" />

This is the screen after click the `full` button and choose data to show

<img src="./imgs/%E6%88%AA%E5%B1%8F2023-11-02%2010.30.34.png" alt="截屏2023-11-02 10.30.34" style="zoom:50%;" />

### Actuator

Like sensor but with a different detail view

<img src="./imgs/%E6%88%AA%E5%B1%8F2023-11-02%2010.31.33.png" alt="截屏2023-11-02 10.31.33" style="zoom:50%;" />

<img src="./imgs/%E6%88%AA%E5%B1%8F2023-11-02%2010.32.02.png" alt="截屏2023-11-02 10.32.02" style="zoom:50%;" />



## 05 Message

This is the page for showing all messages received from device (simulator)

There are three options:

- **Type**: for which kind device
- **Level**: message level (info, warning, error)
- **Date**: the time the message sent

After querying, the result will be shown below. If you want to see `message` and `data` more clearly, you can hover the tag.

<img src="./imgs/%E6%88%AA%E5%B1%8F2023-11-02%2010.33.14.png" alt="截屏2023-11-02 10.33.14" style="zoom:50%;" />



## 06 User

### List

The page showing all users, path `User/UserList`

Functions are similar to `Device`

<img src="./imgs/%E6%88%AA%E5%B1%8F2023-11-02%2010.36.10.png" alt="截屏2023-11-02 10.36.10" style="zoom:50%;" />

### Add

> P.S.: The normal user can not use this page

Path `User/UserAdd`

After entering the information and click add, there will be a new user

<img src="./imgs/%E6%88%AA%E5%B1%8F2023-11-02%2010.38.33.png" alt="截屏2023-11-02 10.38.33" style="zoom:50%;" />

### Edit

Click the edit button on `User/UserList` page to enter.

Like add page, enter the information and click edit

> P.S.: `username` can not be edited.

<img src="./imgs/%E6%88%AA%E5%B1%8F2023-11-02%2010.39.56.png" alt="截屏2023-11-02 10.39.56" style="zoom:50%;" />



## FAQ

None