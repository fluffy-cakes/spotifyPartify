provider "azurerm" {
    features {}
}


data "azurerm_resource_group" "rg" {
    name                               = "partify"
}


data "azurerm_container_registry" "registry" {
    name                               = "pmackpartyapp"
    resource_group_name                = data.azurerm_resource_group.rg.name
}


resource "azurerm_container_group" "container" {
    name                               = "partify"
    location                           = data.azurerm_resource_group.rg.location
    resource_group_name                = data.azurerm_resource_group.rg.name
    ip_address_type                    = "Public"
    dns_name_label                     = "pmackpartyapp"
    os_type                            = "Linux"
    restart_policy                     = "Always"

    container {
        name                           = "partifyfront"
        image                          = "${data.azurerm_container_registry.registry.login_server}/partifyfront"
        cpu                            = "2"
        memory                         = "8"

        ports {
            port                       = 80
            protocol                   = "TCP"
        }

        environment_variables          = {
            WEDDING_USERS              = file("${path.module}/users.json")
        }
    }

    exposed_port {
        port                           = 80
        protocol                       = "TCP"
    }


    container {
        name                           = "partifyback"
        image                          = "${data.azurerm_container_registry.registry.login_server}/partifyback"
        cpu                            = "2"
        memory                         = "8"

        ports {
            port                       = 5000
            protocol                   = "TCP"
        }

        environment_variables          = {
            SPOTIPY_REDIRECT_URI       = "http://127.0.0.1:5000/"
            FLASK_RUN_HOST             = "localhost"
        }

        secure_environment_variables   = {
            CACHED_TOKEN               = file("${path.module}/cached_token")
            SPOTIPY_CLIENT_ID          = ""
            SPOTIPY_CLIENT_SECRET      = ""
        }
    }


    image_registry_credential {
        password                       = data.azurerm_container_registry.registry.admin_password
        server                         = data.azurerm_container_registry.registry.login_server
        username                       = data.azurerm_container_registry.registry.admin_username
    }
}