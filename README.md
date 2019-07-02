# UTM30LXEW_init
This repository present an experimental characterization of a Hokuyo LiDAR UTM30LX-EW running with ROS.
## Presentation
This Repository is this repository is organized as follows:
-- [UTM30LXEW_init.md](https://github.com/Tilaguy/UTM30LXEW_init/blob/master/README.md) ->
## 1. ROS installing on Raspberry Pi 3 [[ROS_inst]]
Raspberry PI 3 runs Raspbian Stretch lite as OS, which you cand download in next link. [Raspbian Stretch](https://www.raspberrypi.org/downloads/raspbian/)

Previos to the ROS installing process, you must be sure that the OS is on the most current version.
```
$ sudo apt-get update
$ sudo apt-get upgarde
```
### 1.1 Preparations
#### 1.1.1 Setup ROS Repositories
For Raspbian Stretch, you must first install dirmngr:
```
$ sudo apt-get install dirmngr
```
Then, you have to select the server direction where you will download the dependences.
```
$ sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
$ sudo apt-key adv --keyserver hkp://ha.pool.sks-keyservers.net:80 --recv-key 421C365BD9FF1F717815A3895523BAEEB01FA116
```
to do again an update and upgrade.
```
$ sudo apt-get update
$ sudo apt-get upgarde
```
#### 1.1.2 Install Bootstrap Dependencies
```
$ sudo apt-get install -y python-rosdep python-rosinstall-generator python-wstool python-rosinstall build-essential cmake
```
#### 1.1.3 Initializing rosdep
```
$ sudo rosdep init
$ rosdep update
```
### 1.2 ROS Installing
The next steps are to install the kinetic ROS on the Raspeberry.
#### 1.2.1 Create a catkin Workspace
In order to build the core packages, you will need a catkin workspace. Create one now:
```
$ mkdir -p ~/ros_catkin_ws
$ cd ~/ros_catkin_ws
```
After that, it will want to fetch the core packages to be able to build them. The package wstool will be used for this. Select the wstool command for the particular variant you want to install: 
- Communication package (recommended):
```
$ rosinstall_generator ros_comm --rosdistro kinetic --deps --wet-only --tar > kinetic-ros_comm-wet.rosinstall
$ wstool init src kinetic-ros_comm-wet.rosinstall
```
- LiDAR package [[Chanel]]:

For the main objective of this project, it is necessary installing the LiDAR ROS package.
```
$ rosinstall_generator urg_node robot_upstart --rosdistro kinetic --deps --wet-only --tar > kinetic-custom_ros.rosinstall
$ wstool merge -t src kinetic-custom_ros.rosinstall
$ wstool update -t src
```
#### 1.2.2 Resolve Dependencies
Before you can build your catkin workspace, you need to make sure that you have all the required dependencies. We use the rosdep tool for this, however, a couple of dependencies are not available in the repositories. They must be manually built first.
```
$ mkdir -p ~/ros_catkin_ws/external_src
$ cd ~/ros_catkin_ws/external_src
$ wget http://sourceforge.net/projects/assimp/files/assimp-3.1/assimp-3.1.1_no_test_models.zip/download -O assimp-3.1.1_no_test_models.zip
$ unzip assimp-3.1.1_no_test_models.zip
$ cd assimp-3.1.1
$ cmake .
$ make
$ sudo make install
```
- Resolving Dependencies with rosdep:

The remaining dependencies should be resolved by running rosdep:
```
$ cd ~/ros_catkin_ws
$ rosdep install -y --from-paths src --ignore-src --rosdistro kinetic -r --os=debian:stretch
```
>>The ```--from-paths``` option indicates that you want to install the dependencies for an entire directory of packages, in this case src.
>>The ```--ignore-src``` option indicates to rosdep that it shouldn't try to install any ROS packages in the src folder from the package manager, you don't need it to since you are building them ourselves.
>>The ```--rosdistro``` option is required because you don't have a ROS environment setup, so we have to indicate to rosdep what version of ROS you are building for.
>>Finally, the ```-y``` option indicates to rosdep that you don't want to be bothered by too many prompts from the package manager.

After a while rosdep will finish installing system dependencies and you can continue. 
- Building the catkin Workspace

Once you have completed downloading the packages and have been resolved the dependencies, you are ready to build the catkin packages.

 Invoke catkin_make_isolated: 
```
$ sudo ./src/catkin/bin/catkin_make_isolated --install -DCMAKE_BUILD_TYPE=Release --install-space /opt/ros/kinetic -j2
```
>>The ```-j2``` instruction is used to avoid an overload of RAM while the equivalent to ```$ catkin_make``` process is running.

Now ROS should be installed! Remember to source the new installation:
```
$ source /opt/ros/kinetic/setup.bash
```
## 2. Used-nodes installing 
Bellow is presented the instructions to install each package necessary to execute the nodes in this project. This is useful to use in every kinetic ROS OS.
### 2.1 install urg_node.
```
$ sudo apt-get install ros-kinetic-urg-node
```
[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)


   [ROS_inst]: <http://wiki.ros.org/indigo/Installation/Source>
   [Chanel]: <https://github.com/JuanDValenciano/channelUI_IoT>
