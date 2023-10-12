


import re




def parse_line(line):
    match = re.match(r'#(\d+)\s*=\s*(\w+)\s*\(\s*\'[^\']*\'\s*,(.+)\)\s*;', line)
    if not match:
        if 'B_SPLINE_SURFACE' in line:
            index_match = re.match(r'#(\d+)', line)
            if not index_match:
                return None
            index = int(index_match.group(1))
            return 'B_SPLINE_SURFACE', index, parse_b_spline_surface(line)
        return None

    index = int(match.group(1))
    data_type = match.group(2)
    data = match.group(3)

    if data_type in ["CARTESIAN_POINT", "DIRECTION"]:
        coords = tuple(float(val) for val in re.findall(r'(-?\d+\.?\d*[eE]?[-+]?\d*)', data))
        return data_type, index, coords

    elif data_type == "VERTEX_POINT":
        vertex = int(re.search(r'#(\d+)', data).group(1))
        return data_type, index, vertex

    elif data_type == "VECTOR":
        components = [comp.strip() for comp in data.split(',')]
        ref_point = int(re.search(r'#(\d+)', components[0]).group(1))
        magnitude = float(components[1])
        return data_type, index, (ref_point, magnitude)

    elif data_type == "AXIS2_PLACEMENT_3D":
        components = [comp.strip() for comp in data.split(',')]
        refs = tuple(int(val) for val in re.findall(r'#(\d+)', data))
        return data_type, index, refs
    
    elif data_type == "LINE":
        points = tuple(int(val) for val in re.findall(r'#(\d+)', data))
        return data_type, index, points

    elif data_type == "CIRCLE":
        components = [comp.strip() for comp in data.split(',')]
        ref_point = int(re.search(r'#(\d+)', components[0]).group(1))
        radius = float(components[1])
        return data_type, index, (ref_point, radius)

    elif data_type == "B_SPLINE_CURVE_WITH_KNOTS":
        # Extract degree
        degree = int(re.search(r'\d+', data).group())
        
        # Use the regex pattern to capture the control points, booleans, knot multiplicities, and knot values
        pattern = r"\(([^)]*)\)[\s,]*\.UNSPECIFIED\.[\s,]*\.(F|T)\.[\s,]*\.(F|T)\.[\s,]*\(([^)]*)\)[\s,]*\(([^)]*)\)"
        matches = re.search(pattern, data)
        
        # If not matched, raise error
        if not matches:
            raise ValueError("Unexpected data format for B_SPLINE_CURVE_WITH_KNOTS")
        
        # Extract control points
        control_points_matches = re.findall(r'#(\d+)', matches.group(1))
        control_points = tuple(map(int, control_points_matches))
        
        # Extract planar and closed booleans
        planar = True if matches.group(2) == "T" else False
        closed = True if matches.group(3) == "T" else False
        
        # Extract knot multiplicities
        knot_multiplicities_matches = re.findall(r'(\d+)', matches.group(4))
        knot_multiplicities = tuple(map(int, knot_multiplicities_matches))
        
        # Extract knot values
        knot_value_matches = re.findall(r'(-?\d+\.\d+e?-?\d+)', matches.group(5))
        knot_values = tuple(map(float, knot_value_matches))
        
        return data_type, index, {
            'degree': degree, 
            'control_points': control_points, 
            'planar': planar, 
            'closed': closed, 
            'knot_multiplicities': knot_multiplicities, 
            'knot_values': knot_values
        }

    elif data_type == "EDGE_CURVE":
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

    elif data_type == "ORIENTED_EDGE":
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
    
    elif data_type == "EDGE_LOOP":
        # Remove newline characters for consistent parsing
        cleaned_data = data.replace('\n', '').replace('\r', '')
        
        # Extract all references between the parentheses
        refs_matches = re.search(r'\(([^)]+)\)', cleaned_data)
        if not refs_matches:
            return None  # or handle this case as needed
        refs_str = refs_matches.group(1)
        refs = tuple(int(val) for val in re.findall(r'#(\d+)', refs_str))
        
        return data_type, index, refs
    
    elif data_type == "PLANE":
        plane = int(re.search(r'#(\d+)', data).group(1))
        return data_type, index, plane

    elif data_type == "CYLINDRICAL_SURFACE":
        components = [comp.strip() for comp in data.split(',')]
        ref_point = int(re.search(r'#(\d+)', components[0]).group(1))
        radius = float(components[1])
        return data_type, index, (ref_point, radius)

    elif data_type == "TOROIDAL_SURFACE":
        components = [comp.strip() for comp in data.split(',')]
        ref_point = int(re.search(r'#(\d+)', components[0]).group(1))
        major_radius = float(components[1])
        minor_radius = float(components[2])
        return data_type, index, (ref_point, major_radius, minor_radius)

    elif data_type == "FACE_BOUND":
        # Remove all newline characters
        cleaned_data = data.replace('\n', '').replace('\r', '')
        
        # Extract the reference using regex
        ref_match = re.search(r'#(\d+)', cleaned_data)
        if not ref_match:
            return None  # or handle this case as needed
        ref = int(ref_match.group(1))
        
        bool_val = ".T." in cleaned_data
        return data_type, index, (ref, bool_val)
    
    elif data_type == "FACE_OUTER_BOUND":
        # Remove all newline characters
        cleaned_data = data.replace('\n', '').replace('\r', '')
        
        # Extract the reference using regex
        ref_match = re.search(r'#(\d+)', cleaned_data)
        if not ref_match:
            return None  # or handle this case as needed
        ref = int(ref_match.group(1))
        
        bool_val = ".T." in cleaned_data
        return data_type, index, (ref, bool_val)

    elif data_type == "ADVANCED_FACE":
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

    elif data_type == "CLOSED_SHELL":
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
    
    elif data_type == "OPEN_SHELL":
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
    
    elif data_type == "MANIFOLD_SOLID_BREP":
        ref_match = re.search(r'#(\d+)', data)
        if ref_match:
            ref = int(ref_match.group(1))
            return data_type, index, ref
        else:
            return None

    elif data_type == "SHELL_BASED_SURFACE_MODEL":
        ref_match = re.search(r'#(\d+)', data)
        if ref_match:
            ref = int(ref_match.group(1))
            return data_type, index, ref
        else:
            return None

    elif data_type == "ADVANCED_BREP_SHAPE_REPRESENTATION":
        components = [comp.strip() for comp in data.split(',')]
        
        # Extract all references from the components
        all_refs = re.findall(r'#(\d+)', data)
        
        if not all_refs or len(all_refs) < 2:
            return None  # Safety check in case we don't get expected data format
        
        refs = tuple(int(val) for val in all_refs[:-1])
        last_ref = int(all_refs[-1])
        
        return data_type, index, (refs, last_ref)
    
    elif data_type == "MANIFOLD_SURFACE_SHAPE_REPRESENTATION":
        components = [comp.strip() for comp in data.split(',')]
        
        # Extract all references from the components
        all_refs = re.findall(r'#(\d+)', data)
        
        if not all_refs or len(all_refs) < 2:
            return None  # Safety check in case we don't get expected data format
        
        refs = tuple(int(val) for val in all_refs[:-1])
        last_ref = int(all_refs[-1])
        
        return data_type, index, (refs, last_ref)
    
    else:   
        return None


def parse_b_spline_surface(line):
    # B_SPLINE_SURFACE extraction
    pattern_bspline = r"B_SPLINE_SURFACE\s*\(\s*(\d+),\s*(\d+),"
    match_bspline = re.search(pattern_bspline, line)
    u_degree = int(match_bspline.group(1))
    v_degree = int(match_bspline.group(2))
    
    # Pattern to capture entire tuple structure
    pattern_control_points_tuple = r"\(\s*(?:#\d+\s*,\s*)*#\d+\s*\)"
        
    # Find all tuples in the line
    tuples_found = re.findall(pattern_control_points_tuple, line)
    control_points = []
    for t in tuples_found:
        # Extract all individual control points from the tuple
        control_points.append([int(x) for x in re.findall(r'#(\d+)', t)])

    # Pattern to capture boolean structure
    pattern_boolean_structure = r"\.UNSPECIFIED\.\s*,\s*\.(F|T)\.\s*,\s*\.(F|T)\.\s*,\s*\.(F|T)\."
    
    # Find all booleans in the line
    booleans_found = re.search(pattern_boolean_structure, line)
    
    closed_u = booleans_found.group(1) == 'T'
    closed_v = booleans_found.group(2) == 'T'
    polynomial = booleans_found.group(3) == 'T'

    # B_SPLINE_SURFACE_WITH_KNOTS extraction
    pattern_knots = r"B_SPLINE_SURFACE_WITH_KNOTS\s*\(\s*\(([^)]*)\s*\),\s*\(([^)]*)\s*\),\s*\(([^)]*)\s*\),\s*\(([^)]*)\s*\),\s*\.UNSPECIFIED\.\s*\)"
    match_knots = re.search(pattern_knots, line)
    if not match_knots:
        raise ValueError(f"Unexpected format for B_SPLINE_SURFACE_WITH_KNOTS in line: {line}")

    u_multiplicities = tuple(map(int, match_knots.group(1).split(',')))
    v_multiplicities = tuple(map(int, match_knots.group(2).split(',')))
    u_knots = tuple(map(float, match_knots.group(3).split(',')))
    v_knots = tuple(map(float, match_knots.group(4).split(',')))

    # RATIONAL_B_SPLINE_SURFACE extraction (optional)
    pattern_rational = r"RATIONAL_B_SPLINE_SURFACE\s*\(\s*\(\s*((\(\s*[+-]?\d+\.\d+(?:e[+-]?\d+)?\s*,\s*[+-]?\d+\.\d+(?:e[+-]?\d+)?\s*,\s*[+-]?\d+\.\d+(?:e[+-]?\d+)?\s*\)\s*,?\s*)+)\)\s*\)"
    match_rational = re.search(pattern_rational, line)
    weights = None
    if match_rational:
        # Here, the goal is to get all numbers from the nested tuples
        raw = re.findall(r'(-?\d+\.\d+e?-?\d+)', match_rational.group(1))
        n = len(control_points)
        m = len(control_points[0])
        weights = []
        for u in range(n):
            weights.append([])
            for v in range(m):
                weights[u].append(raw[v])

    return {
        'type': 'BOUNDED_SURFACE B_SPLINE_SURFACE',
        'u_degree': u_degree,
        'v_degree': v_degree,
        'control_points': control_points,
        'closed_u': closed_u,
        'closed_v': closed_v,
        'polynomial': polynomial,
        'u_multiplicities': u_multiplicities,
        'v_multiplicities': v_multiplicities,
        'u_knots': u_knots,
        'v_knots': v_knots,
        'weights': weights
    }


def parse_step_file(filename):
    cartesian_points = {}
    directions = {}
    vertex_points = {}
    vectors = {}
    axis2_place_3D = {}
    lines = {}
    circles = {}
    b_spline_curves = {}
    edge_curve = {}
    oriented_edge = {}
    edge_loop = {}
    planes = {}
    cyl_surf = {}
    tor_surf = {}
    b_spline_surf = {}
    face_bound = {}
    face_out_bound = {}
    adv_face = {}
    closed_shell = {}
    open_shell = {}
    man_solid_brep = {}
    sh_based_surf_mod = {}
    adv_brep_shape_rep = {}
    man_surf_shape_rep = {}

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
                    elif data_type == "VECTOR":
                        vectors[index] = data
                    elif data_type == "AXIS2_PLACEMENT_3D":
                        axis2_place_3D[index] = data 
                    elif data_type == "LINE":
                        lines[index] = data
                    elif data_type == "CIRCLE":
                        circles[index] = data 
                    elif data_type == "B_SPLINE_CURVE_WITH_KNOTS":
                        b_spline_curves[index] = data
                    elif data_type == "EDGE_CURVE":
                        edge_curve[index] = data 
                    elif data_type == "ORIENTED_EDGE":
                        oriented_edge[index] = data 
                    elif data_type == "EDGE_LOOP":
                        edge_loop[index] = data 
                    elif data_type == "PLANE":
                        planes[index] = data 
                    elif data_type == "CYLINDRICAL_SURFACE":
                        cyl_surf[index] = data 
                    elif data_type == "TOROIDAL_SURFACE":
                        tor_surf[index] = data 
                    elif data_type == "B_SPLINE_SURFACE":
                        b_spline_surf[index] = data 
                    elif data_type == "FACE_BOUND":
                        face_bound[index] = data 
                    elif data_type == "FACE_OUTER_BOUND":
                        face_out_bound[index] = data 
                    elif data_type == "ADVANCED_FACE":
                        adv_face[index] = data 
                    elif data_type == "CLOSED_SHELL":
                        closed_shell[index] = data 
                    elif data_type == "OPEN_SHELL":
                        open_shell[index] = data 
                    elif data_type == "MANIFOLD_SOLID_BREP":
                        man_solid_brep[index] = data 
                    elif data_type == "SHELL_BASED_SURFACE_MODEL":
                        sh_based_surf_mod[index] = data 
                    elif data_type == "ADVANCED_BREP_SHAPE_REPRESENTATION":
                        adv_brep_shape_rep[index] = data 
                    elif data_type == "MANIFOLD_SURFACE_SHAPE_REPRESENTATION":
                        man_surf_shape_rep[index] = data 
                
                entry = ""  # Reset the entry for the next round

    return {
        "CARTESIAN_POINT": cartesian_points,
        "DIRECTION": directions,
        "VERTEX_POINT": vertex_points,
        "VECTOR": vectors,
        "AXIS2_PLACEMENT_3D": axis2_place_3D,
        "LINE": lines,
        "CIRCLE": circles,
        "B_SPLINE_CURVE_WITH_KNOTS": b_spline_curves,
        "EDGE_CURVE": edge_curve,
        "ORIENTED_EDGE": oriented_edge,
        "EDGE_LOOP": edge_loop,
        "PLANE": planes,
        "CYLINDRICAL_SURFACE": cyl_surf,
        "TOROIDAL_SURFACE": tor_surf,
        "B_SPLINE_SURFACE": b_spline_surf,
        "FACE_BOUND": face_bound,
        "FACE_OUTER_BOUND": face_out_bound,
        "ADVANCED_FACE": adv_face,
        "CLOSED_SHELL": closed_shell,
        "OPEN_SHELL": open_shell,
        "MANIFOLD_SOLID_BREP": man_solid_brep,
        "SHELL_BASED_SURFACE_MODEL": sh_based_surf_mod,
        "ADVANCED_BREP_SHAPE_REPRESENTATION": adv_brep_shape_rep,
        "MANIFOLD_SURFACE_SHAPE_REPRESENTATION": man_surf_shape_rep,
    }

filename = "test_part3_AP214.step"
parsed_data = parse_step_file(filename)
#for var in parsed_data:
#    print('\n', var, '{')
#    for key in parsed_data[var]:
#        print(str(key)+': ', parsed_data[var][key])
#    print('}')
for key, value in parsed_data.items():
    print(key, value)
    print('\n')


