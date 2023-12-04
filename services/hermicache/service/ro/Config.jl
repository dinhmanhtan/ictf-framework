struct Config
    redis_host::String
    host::String
    port::Int32
end

function prod_config()
    if !haskey(ENV, "REDIS_HOST")
        throw("Env variable 'REDIS_HOST' must be defined")
    end

    host = ENV["REDIS_HOST"]
    prod_config = Config(host, "0.0.0.0", 8080)
    
    return prod_config
end

dev_config = Config("localhost", "127.0.0.1", 8080)


function get_config()
    if !haskey(ENV, "ENV")
        throw("Env variable 'ENV' must be defined ('PROD' or 'DEV')")
    end

    if ENV["ENV"] == "PROD"
        return prod_config()
    elseif ENV["ENV"] == "DEV"
        return dev_config
    else
        throw("Unknown env type '" * ENV["ENV"] * "'")
    end
end
