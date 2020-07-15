Made by ***Team YUMIT***, for a better, green future. :deciduous_tree: 

**To check out our web application, click on this [link](https://mighty-mit.herokuapp.com/).**

- **[Click here](https://drive.google.com/file/d/1GeTh9ag28rgVvaUe2rZh8kdqNqLD5Rs2/view?usp=sharing) to see the documentation of our project.**

- **[Click here](https://drive.google.com/file/d/1kY-niv9kU3Jquc3cabrvWrytKa1_y7fi/view) to check out our video presentation for the project. For web application demo, please skip to 2:36 in the video.**

- **[Click here](https://drive.google.com/file/d/1yd6g79vODjzk3qt0cpVAwvl3IoW8qM7u/view) to see our PowerPoint Presentation for the project.**

# Overview

As the world moves forward, renewable energy sources will play a crucial role in promoting a green, sustainable society and hence, will directly impact on the health and well-being of all humans across Earth.

![Global Wind Power cumulative](https://upload.wikimedia.org/wikipedia/commons/thumb/1/1d/Global_Wind_Power_Cumulative_Capacity.svg/720px-Global_Wind_Power_Cumulative_Capacity.svg.png)

Renewable sources are expected to make about 45 per cent of the global electricity demand by 2040. Today, wind energy accounts for 651 GW of electrical power, which accounts for more than 5% of global demand. With the continuous, exponential growth of wind farms and the development of more efficient wind turbines, the impact and contribution of wind energy for energy is only going to increase. Therefore, there is an ever-increasing need for a solution which can efficiently integrate various conventional power sources with wind farms to reduce overproduction by conventional sources which can unnecessarily contribute towards pollution. By collaborating traditional and renewable sources, we can efficiently match demand with supply without excessive production and therefore save up on monetary assets as well.

![Wind power around the world](https://i.imgur.com/fGzoPtF.png)

# Existing Problem

Levels of production of wind energy are hard to predict as they rely on potentially unstable weather conditions present at the wind farm. In particular, wind speed is crucial for energy production based on wind, and it may vary drastically over time. 

Energy suppliers are interested in accurate predictions, as they can avoid overproduction by coordinating the collaborative production of traditional power plants and weather-dependent energy sources. This will ultimately result in substantial monetary saving.

# Proposed Solution

The objective of our proposed solution is to provide our client with a novel, pragmatic solution for better collaboration between wind farms and conventional energy sources. Our motive is to ensure that the energy demand and supply is efficiently optimized so as to minimize overproduction and monetary loss. 

The approach combines teamwork, knowledge of various domains and advanced simulation to help wind farm and electric power grid operators. We have incorporated multiple components of our solution into a single, fluid, web-based user interface that will accurately predict the power output of the wind turbine, given the current weather conditions, for the next 72 hours.

Our solution consists of two components which have been integrated for a holistic and complete energy management system for efficient collaboration between wind farms and conventional sources of electricity. 

![Flowchart](https://i.imgur.com/4iSELDO.png)

## (a) The LSTM Neural Network model

After testing multiple Neural Network algorithms, we decided to finalize Long Short Term Memory (LSTM) for predicting the power output of the turbines. LSTM being a type of Recurrent Neural Network is an algorithm which is efficient for time series forecasting, wherein you require long term dependencies. This was crucial for our project as we were required to predict the power output given a set of previous and present weather information. As LSTM is very capable of handling data for long periods, which is required in our case, it performed much better for the same data set than other machine learning models like linear regression, logistic regression etc. 

![Model layers](https://i.imgur.com/ybG5UIz.png)

We selected "Adam" as our optimizer due to the fact it performs much better than Root mean square(RMS prop) and the weighted mean average for data with a lot of noise/sparse gradients ( which is generally the case for weather data sets). Adam was also chosen as it is computationally very efficient as well.

For our loss function, we went with "Mean Absolute Error" as it gave better accuracy and took less to optimize the model when compared to  Mean Square error.

A total of 250 epochs were performed on the data set.

![Loss graph](https://i.imgur.com/t4XnOje.png)

The data set was compiled using the Supervisory Control and Data Acquisition (SCADA) system integrated with modern wind turbines. It consisted of 1,05,120 rows of multi-variate data. After careful evaluation of inter dependencies of the various variables using graphical and statistical methods, it was concluded that the Active power output of the wind turbines had a maximum correlation with Wind speed and wind direction. To reduce the complexity of the model, other variables were dropped. The data set was then split into the training data, which amounted to 52,561 rows of data and test data, which amounted to 52,559 rows of data. For predictions, a window of five days weather data was taken as input. For each hour, one set of data was recorded, totaling to 120 weather input. An output prediction of 12 hours is given using the provided data. For each hour, six predictions for every ten minutes is made, totaling to 72 active power output predictions for the next 12 hours. 

## (b) Web-Based Application

To make our Machine Learning model user friendly and help the client to visualize the output better, we have created a Web Application using Flask, which will be deployed on Heroku. The web-app will have three sections, Home Page, About Page and Statistics Page. We have used the [OpenWeatherMap API](https://openweathermap.org/api) to get the current and historical data (Code snippet for real time data collection shown in the picture). The trained ML model has been embedded into our application which will directly use the data received from the API and show the predicted output on the Home page.

1. **The Home page** will have the information about the current weather status and will show a graph of expected power output for the next 72 hours as predicted by our ML model. This webpage will also have a section for the user to enter a few parameters, such as wind speed and direction, that will allow the user to get a rough estimate of output power from the wind turbine for the given condition.

![Home Page](https://i.imgur.com/caNwDMP.jpg)

2. **The About page** will have the information and details regarding wind energy, how it is being produced and some general facts. We will also mention the approach used by us and how it would help the client. Information of the IBM Hack Challenge and the team behind the project would be included as well.

3. **The Statistics page** will have statistics about the power generated in the past based on the data analysis that we have done. The webpage will also have graphs which will make the numbers more interpretable and visually informative. It would plots which would correlations between various variables such as wind speed, wind direction, power output etc. Furthermore, it will also display the power generated each hour in the future in the form of a table. 

![Stats Page](https://i.imgur.com/HZNtLbl.png)

# Future Scope

If deployed at an industrial scale, with an improvement in hardware, the accuracy of the model can be vastly improved by extensive experimentation including but not restricted to, adding more LSTM layers, changing the number of nodes per layer, increasing the number of epochs, trying a variety of optimisers and loss functions to reduce the loss.

Furthermore, with the use of an API and a dataset providing comprehensive and a wide variety of features, the input to the neural network can be made more diverse, which will ultimately improve the robustness of the model.

Also, by utilising weather, solar and hydro database from multiple cities, it is possible to create a multi-city system, which can monitor and predict the total power output from all these renewable sources of energy. 

We have set the base of such a system by creating a login and a dummy registration page. Using this feature, multiple clients and users from various parts of the world can register themselves by putting in their details such as their location and ZIP code. Using this information, our application can automatically import the required weather data if it is available in the API's database and therefore can predict the Windpower output for wind farm situated in that region.
