# -*- coding: UTF-8 -*-
import pprint
import androidhelper  #导入安卓API库

droid=androidhelper.Android()
apps=droid.getLaunchableApplications()
print(apps.result["WebDriver"])
pprint.pprint(apps.result)
print('-------------------------------------')
pacs=droid.getRunningPackages()
pprint.pprint(pacs.result)  
