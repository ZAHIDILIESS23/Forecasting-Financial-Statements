#!/usr/bin/env python
# coding: utf-8

# # Forecasting Financial Statements with `finstmt`
# 
# First import the necessary classes and `pandas`.

# In[1]:


from finstmt import FinancialStatements, IncomeStatements, BalanceSheets
import pandas as pd


# In[3]:


get_ipython().system(' pip install finstmt')


# ## Load Financial Statements

# In[2]:


inc_df = pd.read_csv('cat_annual_income.csv', index_col=0)
bs_df = pd.read_csv('cat_annual_bs.csv', index_col=0)

bs = BalanceSheets.from_df(bs_df)
inc = IncomeStatements.from_df(inc_df)
stmts = FinancialStatements(inc, bs)


# ### View Existing Statements

# In[3]:


stmts


# ### Copy the Statements
# 
# To set up for running multiple forecasts off the same data, you can make a copy of it using `stmts.copy()`. Then any adjustments to the configuration will only be in the original object and not the copy.

# In[5]:


stmts.config.update_all(['forecast_config', 'method'], 'auto')


# In[6]:


fcst_stmts = stmts.forecast(periods=12)


# In[ ]:


fcst_stmts


# In[8]:


stmts2 = stmts.copy()


# ## Run a Forecast

# ### Set the Default Method
# 
# This is not a necessary step, but this is the way to change the default forecast method. The default is already `cagr` and so this doesn't actually have an effect.

# In[9]:


stmts.config.update_all(['forecast_config', 'method'], 'cagr')


# ## View the Forecast Assumptions
# 
# All the assumptions going into the forecast are in `forecast_assumptions`:

# In[10]:


stmts.forecast_assumptions


# ### Run the First Forecast
# 
# Forecasts are run using `.forecast()` and produce `ForecastedFinancialStatements`. It is usually good practice to first run a forecast, then view the results, then adjust as needed.

# In[11]:


fcst = stmts.forecast()


# > Note: Warnings are raised because CAGR is the default method but it is not suitable for items which begin with 0
# 
# Now view the forecast.

# In[12]:


fcst


# And the plot:

# In[13]:


fcst.plot()


# It is also possible to plot a subset. Let's focus on only a few items for sake of example.

# In[14]:


fcst.plot(subset=['revenue', 'cogs', 'cash'])


# ### Change Methods and Re-Run Forecast
# 
# After viewing the plots, the appropriate methods for forecasting each item should be chosen. Then they can be updated.

# In[15]:


stmts.config.update('revenue', ['forecast_config', 'method'], 'trend')
stmts.config.update('cogs', ['forecast_config', 'method'], 'mean')


# Now re-run the forecast.

# In[16]:


fcst = stmts.forecast()


# And plot the results:

# In[17]:


fcst.plot(subset=['revenue', 'cogs', 'cash'])


# Now the methods for those forecasts has been updated.
# 
# ### Adjusting an Existing Forecast
# 
# While it is possible to use the `manual` forecast type and pass in the desired growth rates or levels from the beginning, it is often more convenient to first run the forecast, then simply adjust it. The `.to_manual` method of the forecast was added for this purpose.
# 
# Either `adjustments` or `replacements` can be passed while updating, and either the level of the item or the growth in the item can be used for the new manual forecast. For either one, a dictionary where the keys are the index of the period and values are the adjustment/replacement or a list containing all the adjustment/replacements can be used.

# In[18]:


fcst.forecasts['cash'].to_manual(adjustments={0: 0.4})  # boost first forecast period cash growth by 40%
fcst.forecasts['cogs'].to_manual(use_levels=True, replacements=[0.85 for _ in range(5)])  # use 85% of sales for full COGS forecast
fcst.forecasts['revenue'].to_manual(use_levels=True, replacements={1: 8e10})  # set second forecast period revenue to 80,000,000,000


# Then just run the forecast again to get everything updated in the statements. Then you can view the plots:

# In[19]:


fcst = stmts.forecast()
fcst.plot(subset=['revenue', 'cogs', 'cash'])


# ## A Second Forecast
# 
# Since we earlier did a `deepcopy` of the `stmts` object, that still has the original forecast assumptions and can be used for a separate forecast.

# In[20]:


stmts2.forecast_assumptions


# In[ ]:




