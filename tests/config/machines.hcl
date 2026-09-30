machines = {                                             
  "machine-01" = {                       
    properties = {                              
      power_type       = "ipmi"
      power_address    = "172.31.31.31"
      power_user       = "Administrator"
      power_boot_type  = "efi"         
      workaround_flags = ["opensesspriv", "authcap", "nochecksumcheck"]
      privilege_level  = "ADMIN"        
      pxe_mac_address  = "aa:bb:cc:11:22:33"                                                                           
      zone             = "zone1"                                                                                    
      domain           = "maas"             
      tags             = ["ceph", "storage"]                                                                           
    }                              
    network_details = {                     
      network_profile = "storage"           
    }                          
    storage_details = {                     
      storage_profile = "ceph-osd"
      devices = {      
        # SAS3908 boot volume, pinned by model+serial
        sdj = { model = "SAS3908", serial = "" }
      }                                              
    }                                                
  }            
}
