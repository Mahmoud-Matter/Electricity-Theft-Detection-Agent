import pandapower as pp
import pandas as pd

def create_egyptian_lv_network():
    """
    This function builds a virtual three-phase low voltage distribution network
    with a manually defined transformer to ensure compatibility.
    """
    # 1. Create an empty electrical network
    net = pp.create_empty_network(name="Egyptian Protection Network")

    # 2. Create main connection points (Buses)
    hv_bus = pp.create_bus(net, vn_kv=11, name="Medium Voltage Station (11kV)")
    lv_bus = pp.create_bus(net, vn_kv=0.4, name="Low Voltage Station (0.4kV)")
    
    pp.create_ext_grid(net, bus=hv_bus)

    # 3. ***** Solution: Define transformer manually *****
    # Instead of using std_type, use create_transformer_from_parameters
    # These are standard technical values for distribution transformers in Egypt
    pp.create_transformer_from_parameters(net, 
                                          hv_bus=hv_bus, 
                                          lv_bus=lv_bus, 
                                          sn_mva=0.4,      # Transformer rating: 400kVA
                                          vn_hv_kv=11,     # Input voltage
                                          vn_lv_kv=0.4,    # Output voltage
                                          vkr_percent=0.9, # Copper resistance
                                          vk_percent=4,    # Total impedance
                                          pfe_kw=0.7,      # Iron loss
                                          i0_percent=0.18) # No-load current

    # 4. Distribute customers on the network
    customer_data = []
    num_customers = 30
    
    for i in range(num_customers):
        if i < 10:
            phase = 'A'
        elif i < 22:
            phase = 'B'
        else:
            phase = 'C'

        customer_bus = pp.create_bus(net, vn_kv=0.4, name=f"Customer Meter {i+1}")
        pp.create_line(net, from_bus=lv_bus, to_bus=customer_bus, length_km=0.005, std_type="NAYY 4x50 SE")
        
        customer_data.append({
            'Customer_ID': i + 1,
            'Bus_ID': customer_bus,
            'Phase': phase
        })

    # 5. Create a DataFrame to map customers to the network
    topology_df = pd.DataFrame(customer_data)

    print("The virtual electrical network has been successfully created!")
    print(f"Total number of customers: {len(net.bus) - 2}")

    return net, topology_df

if __name__ == '__main__':
    net, topology_df = create_egyptian_lv_network()
    
    print("\n--- Network Summary ---")
    print(net)
    
    print("\n--- Sample of Customer Mapping (first 5 customers) ---")
    print(topology_df.head())
