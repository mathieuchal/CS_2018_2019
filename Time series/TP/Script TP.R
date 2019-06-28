library("ggplot")
library('forecast')
library('tseries')
library('MLmetrics')

setwd('/Users/chalvidalm/Documents/3A OMA/S??ries chronologiques')
data <- read.table('0219_td_centrale.csv',header=TRUE, sep = ";")

data$earning_yield = data$earnings/data$price


ggplot(data = data, aes(rates, earning_yield)) + geom_point() + geom_smooth(method='lm')
reg = lm(data$earning_yield ~ data$rates)

data$MCO = reg$coefficients[1] + reg$coefficients[2]*data$rates
  
#4 - appel des 3 tests statistiques
t.test(data$earning_yield, data$MCO)
fisher.test(data$earning_yield[0:10], data$MCO[0:10])
summary(reg)$r.squared

#5
plot(density(reg$residuals))
qqnorm(reg$residuals);qqline(reg$residuals)
acf(reg$residuals)
plot(data$MCO,reg$residuals,main="Residuals vs. fitted")
abline(h=0,col="red")

#6 
data$deflated<- rep(NaN,nrow(data))
data$deflated[13:nrow(data)] <- (data$cpi[1:(nrow(data)-12)]-data$cpi[13:nrow(data)])*100/data$cpi[13:nrow(data)]

data$real_rates<-data$rates-data$deflated
ggplot(data = data, aes(real_rates, earning_yield)) + geom_point() + geom_smooth(method='lm')
reg_real = lm(data$earning_yield ~ data$real_rates)

#8
acf(data$earning_yield)
pacf(data$earning_yield)

differentiation <- diff(data$earning_yield, differences = 1)
acf(differentiation)
pacf(differentiation)

auto.arima(data$earning_yield)

#9-10

#model <- arma(data$earning_yield, order = c(1, 5))

model <- arima(data$earning_yield, order=c(1,1,0), method="ML")
prediction <- predict(model, 10, se.fit=TRUE)

up_ <- prediction$pred + 1.96*prediction$se
lo_ <- prediction$pred - 1.96*prediction$se
plot(prediction$pred)
prediction_df <- data.frame(list(prediction$pred, up_,lo_))
matplot(prediction_df, )

#11
model <- arima(data$earning_yield[1:(nrow(data)-3)], order=c(1,1,0), method="ML")
prediction <- predict(model, 3, se.fit=TRUE)

MSE(prediction$pred, data$earning_yield[(nrow(data)-2):nrow(data)])

RMSE(prediction$pred, data$earning_yield[(nrow(data)-2):nrow(data)])

#12 

