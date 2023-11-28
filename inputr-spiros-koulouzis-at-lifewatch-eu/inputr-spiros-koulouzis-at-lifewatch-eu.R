setwd('/app')

# retrieve input parameters

library(optparse)
library(jsonlite)

option_list = list

option_list = list(
make_option(c("--id"), action="store", default=NA, type='character', help="my description")
)

# set input parameters accordingly
opt = parse_args(OptionParser(option_list=option_list))


id = opt$id






param_api_key = 'SECRET'

a = 2
b = a + 1

msg = "Hello world!"



# capturing outputs
file <- file(paste0('/tmp/msg_', id, '.json'))
writeLines(toJSON(msg, auto_unbox=TRUE), file)
close(file)
