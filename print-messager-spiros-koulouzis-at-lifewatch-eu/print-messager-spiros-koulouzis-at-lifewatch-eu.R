setwd('/app')

# retrieve input parameters

library(optparse)
library(jsonlite)

option_list = list

option_list = list(
make_option(c("--id"), action="store", default=NA, type='character', help="my description"),
make_option(c("--msg"), action="store", default=NA, type='character', help="my description"),
make_option(c("--param_api_key"), action="store", default=NA, type='character', help="my description")
)

# set input parameters accordingly
opt = parse_args(OptionParser(option_list=option_list))


id = opt$id
msg = opt$msg

param_api_key = opt$param_api_key





print(param_api_key)
print(msg)



