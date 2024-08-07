import graphviz


def create_concept_map(format: str, output_file_name_wo_ext: str) -> bool:
    """
    Create a simple graph using the Graphviz library and save it to a file.

    Args:
        format (str): The format of the output file ('png' or 'svg').
        output_file_name_wo_ext (str): The name of the output file without the file extension.

    Returns:
        bool: True if the graph is successfully created and saved, False otherwise.
    """
    assert format in ['png', 'svg'], 'Invalid graph type'
    try:
        # Create a new Digraph object
        dot = graphviz.Digraph(comment='Advanced Graph')

        # Set the graph background color to transparent
        dot.attr(bgcolor='transparent')

        node_bg_color = '#202123' 
        white = '#F7F7F7'
        # Add nodes with different shapes and styles
        dot.node('A', 'Some title', shape='box', style='filled', color='#F2045D', fontname='SF Pro Display Bold', fontsize='14', fontcolor=white)
        dot.node('B', 'Process', shape='box', style='filled', color=node_bg_color, fontname='SF Pro Display Bold', fontsize='14', fontcolor=white)
        dot.node('C', 'Process', shape='box', style='filled', color=node_bg_color, fontname='SF Pro Display Bold', fontsize='14', fontcolor=white)
        dot.node('BA', 'Process LL', shape='box', style='filled', color=node_bg_color, fontname='SF Pro Display Bold', fontsize='14', fontcolor=white)
        dot.node('BB', 'Process LR', shape='box', style='filled', color=node_bg_color, fontname='SF Pro Display Bold', fontsize='14', fontcolor=white)
        dot.node('CA', 'Process RL', shape='box', style='filled', color=node_bg_color, fontname='SF Pro Display Bold', fontsize='14', fontcolor=white)
        dot.node('CB', 'Process RR', shape='box', style='filled', color=node_bg_color, fontname='SF Pro Display Bold', fontsize='14', fontcolor=white)

        # Add edges with labels
        dot.edge('A', 'B', color=node_bg_color, style='invis', penwidth='2', arrowhead='none')
        dot.edge('A', 'C', color=node_bg_color, style='invis', penwidth='2', arrowhead='none')
        dot.edge('B', 'BA', color=node_bg_color, style='invis', penwidth='2', arrowhead='none')
        dot.edge('B', 'BB', color=node_bg_color, style='invis', penwidth='2', arrowhead='none')
        dot.edge('C', 'CA', color=node_bg_color, style='invis', penwidth='2', arrowhead='none')
        dot.edge('C', 'CB', color=node_bg_color, style='invis', penwidth='2', arrowhead='none')

        # Render the graph to a file
        dot.render(output_file_name_wo_ext, format=format)
        return True
    except Exception as e:
        print(f'Error: {e}')
        return False

create_concept_map('svg', 'test')
