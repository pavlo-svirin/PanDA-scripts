# plugins for Adder. format=vo1(|vo2(vo3...):moduleName:className(,vo4...)
adder_plugins = local|lsst:dataservice.AdderLQCDPlugin:AdderLQCDPlugin

# plugins for Setupper. format=vo1(|vo2(vo3...):moduleName:className(,vo4...)
#setupper_plugins = local:dataservice.SetupperDummyPlugin:SetupperDummyPlugin
setupper_plugins = local|lsst:dataservice.SetupperLQCDPlugin:SetupperLQCDPlugin
