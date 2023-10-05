import re

def parse_line(line):
    match = re.match(r'#(\d+)\s*=\s*(\w+)\s*\(\s*\'[^\']*\'\s*,(.+)\)\s*;', line)
    if not match:
        return None

    index = int(match.group(1))
    data_type = match.group(2)
    data = match.group(3)

    if data_type in ["CARTESIAN_POINT", "DIRECTION"]:
        coords = tuple(float(val) for val in re.findall(r'(-?\d+\.?\d*[eE]?[-+]?\d*)', data))
        return data_type, index, coords

    if data_type == "VERTEX_POINT":
        vertex = int(re.search(r'#(\d+)', data).group(1))
        return data_type, index, vertex

    if data_type == "LINE":
        points = tuple(int(val) for val in re.findall(r'#(\d+)', data))
        return data_type, index, points

    if data_type == "B_SPLINE_CURVE_WITH_KNOTS":
        # Extract degree
        degree = int(re.search(r'\d+', data).group())
    
        # Use the regex pattern to capture the control points, knot multiplicities, and knot values
        pattern = r"\(([^)]*)\)[\s,]*\.UNSPECIFIED\.[\s,]*\.F\.[\s,]*\.F\.[\s,]*\(([^)]*)\)[\s,]*\(([^)]*)\)"
        matches = re.search(pattern, data)
    
        # If not matched, raise error
        if not matches:
            raise ValueError("Unexpected data format for B_SPLINE_CURVE_WITH_KNOTS")
    
        # Extract control points
        control_points_matches = re.findall(r'#(\d+)', matches.group(1))
        control_points = tuple(map(int, control_points_matches))
    
        # Extract knot multiplicities
        knot_multiplicities_matches = re.findall(r'(\d+)', matches.group(2))
        knot_multiplicities = tuple(map(int, knot_multiplicities_matches))
    
        # Extract knot values
        knot_value_matches = re.findall(r'(-?\d+\.\d+e?-?\d+)', matches.group(3))
        knot_values = tuple(map(float, knot_value_matches))
    
        return data_type, index, {'degree': degree, 'control_points': control_points, 'knot_multiplicities': knot_multiplicities, 'knot_values': knot_values}

    if data_type == "CIRCLE":
        components = [comp.strip() for comp in data.split(',')]
        ref_point = int(re.search(r'#(\d+)', components[0]).group(1))
        radius = float(components[1])
        return data_type, index, (ref_point, radius)

    if data_type == "ADVANCED_BREP_SHAPE_REPRESENTATION":
        components = [comp.strip() for comp in data.split(',')]
        
        # Extract all references from the components
        all_refs = re.findall(r'#(\d+)', data)
        
        if not all_refs or len(all_refs) < 2:
            return None  # Safety check in case we don't get expected data format
        
        refs = tuple(int(val) for val in all_refs[:-1])
        last_ref = int(all_refs[-1])
        
        return data_type, index, (refs, last_ref)
    
    if data_type == "AXIS2_PLACEMENT_3D":
        components = [comp.strip() for comp in data.split(',')]
        refs = tuple(int(val) for val in re.findall(r'#(\d+)', data))
        return data_type, index, refs
    
    if data_type == "MANIFOLD_SOLID_BREP":
        ref_match = re.search(r'#(\d+)', data)
        if ref_match:
            ref = int(ref_match.group(1))
            return data_type, index, ref
        else:
            return None

    if data_type == "CLOSED_SHELL":
        # Remove all newline characters
        cleaned_data = data.replace('\n', '').replace('\r', '')
        
        # Find the indices of the opening and closing parentheses
        start_idx = cleaned_data.find('(')
        end_idx = cleaned_data.rfind(')')
        
        if start_idx != -1 and end_idx != -1:
            # Extract the content between the parentheses
            refs_str = cleaned_data[start_idx+1:end_idx]
            
            # Extract the individual references
            refs = tuple(map(int, re.findall(r'#(\d+)', refs_str)))
            return data_type, index, refs
        else:
            return None
    
    if data_type == "ADVANCED_FACE":
        # Remove all newline characters
        cleaned_data = data.replace('\n', '').replace('\r', '')
        
        # Find the indices of the opening and closing parentheses for the ref values
        start_idx = cleaned_data.find('(')
        end_idx = cleaned_data.find(')', start_idx)
        
        if start_idx != -1 and end_idx != -1:
            # Extract the content between the parentheses
            refs_str = cleaned_data[start_idx+1:end_idx]
            
            # Extract the individual references
            refs = tuple(map(int, re.findall(r'#(\d+)', refs_str)))
        else:
            return None  # or handle this case as needed
        
        last_ref_match = re.search(r'#(\d+)', cleaned_data[end_idx:])
        if not last_ref_match:
            return None  # or handle this case as needed
        last_ref = int(last_ref_match.group(1))
        
        bool_val = ".T." in cleaned_data[end_idx:]
        return data_type, index, (*refs, last_ref, bool_val)

    if data_type == "FACE_BOUND":
        # Remove all newline characters
        cleaned_data = data.replace('\n', '').replace('\r', '')
        
        # Extract the reference using regex
        ref_match = re.search(r'#(\d+)', cleaned_data)
        if not ref_match:
            return None  # or handle this case as needed
        ref = int(ref_match.group(1))
        
        bool_val = ".T." in cleaned_data
        return data_type, index, (ref, bool_val)
    
    if data_type == "EDGE_LOOP":
        # Remove newline characters for consistent parsing
        cleaned_data = data.replace('\n', '').replace('\r', '')
        
        # Extract all references between the parentheses
        refs_matches = re.search(r'\(([^)]+)\)', cleaned_data)
        if not refs_matches:
            return None  # or handle this case as needed
        refs_str = refs_matches.group(1)
        refs = tuple(int(val) for val in re.findall(r'#(\d+)', refs_str))
        
        return data_type, index, refs
    
    if data_type == "ORIENTED_EDGE":
        components = [comp.strip() for comp in data.split(',')]
    
        # Extracting refs
        try:
            ref1 = int(components[0][1:]) if "#" in components[0] else None
            ref2 = int(components[1][1:]) if "#" in components[1] else None
            ref3 = int(components[2][1:]) if "#" in components[2] else None
        except ValueError:
            return None
    
        bool_val = components[3] == ".T."
        result = (ref1, ref2, ref3, bool_val)
        return data_type, index, result
    
    if data_type == "EDGE_CURVE":
        components = [comp.strip() for comp in data.split(',')]
    
        # Extracting refs
        try:
            ref1 = int(components[0][1:]) if "#" in components[0] else None
            ref2 = int(components[1][1:]) if "#" in components[1] else None
            ref3 = int(components[2][1:]) if "#" in components[2] else None
        except ValueError:
            return None

        bool_val = components[3] == ".T."
        result = (ref1, ref2, ref3, bool_val)
        return data_type, index, result

    return None

def parse_step_file(filename):
    cartesian_points = {}
    directions = {}
    vertex_points = {}
    lines = {}
    b_spline_curves = {}
    circles = {}
    adv_brep_shape_rep = {}
    axis2_place_3D = {}
    man_solid_brep = {}
    closed_shell = {}
    adv_face = {}
    face_bound = {}
    edge_loop = {}
    oriented_edge = {}
    edge_curve = {}

    with open(filename, 'r') as f:
        entry = ""
        for line in f:
            entry += line.strip()
            if ';' in line:  # Indicates the end of an entry
                parsed_data = parse_line(entry)
                if parsed_data:
                    data_type, index, data = parsed_data

                    if data_type == "CARTESIAN_POINT":
                        cartesian_points[index] = data
                    elif data_type == "DIRECTION":
                        directions[index] = data
                    elif data_type == "VERTEX_POINT":
                        vertex_points[index] = data
                    elif data_type == "LINE":
                        lines[index] = data
                    elif data_type == "B_SPLINE_CURVE_WITH_KNOTS":
                        b_spline_curves[index] = data
                    elif data_type == "CIRCLE":
                        circles[index] = data 
                    elif data_type == "ADVANCED_BREP_SHAPE_REPRESENTATION":
                        adv_brep_shape_rep[index] = data 
                    elif data_type == "AXIS2_PLACEMENT_3D":
                        axis2_place_3D[index] = data 
                    elif data_type == "MANIFOLD_SOLID_BREP":
                        man_solid_brep[index] = data 
                    elif data_type == "CLOSED_SHELL":
                        closed_shell[index] = data 
                    elif data_type == "ADVANCED_FACE":
                        adv_face[index] = data 
                    elif data_type == "FACE_BOUND":
                        face_bound[index] = data 
                    elif data_type == "EDGE_LOOP":
                        edge_loop[index] = data 
                    elif data_type == "ORIENTED_EDGE":
                        oriented_edge[index] = data 
                    elif data_type == "EDGE_CURVE":
                        edge_curve[index] = data 
                
                entry = ""  # Reset the entry for the next round

    return {
        "CARTESIAN_POINT": cartesian_points,
        "DIRECTION": directions,
        "VERTEX_POINT": vertex_points,
        "LINE": lines,
        "B_SPLINE_CURVE_WITH_KNOTS": b_spline_curves,
        "CIRCLE": circles,
        "ADVANCED_BREP_SHAPE_REPRESENTATION": adv_brep_shape_rep,
        "AXIS2_PLACEMENT_3D": axis2_place_3D,
        "MANIFOLD_SOLID_BREP": man_solid_brep,
        "CLOSED_SHELL": closed_shell,
        "ADVANCED_FACE": adv_face,
        "FACE_BOUND": face_bound,
        "EDGE_LOOP": edge_loop,
        "ORIENTED_EDGE": oriented_edge,
        "EDGE_CURVE": edge_curve
    }

filename = "test_part3_FreeCAD.step"
parsed_data = parse_step_file(filename)
for key, value in parsed_data.items():
    print(key, value)

