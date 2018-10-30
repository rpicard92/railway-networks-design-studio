"""
This is where the implementation of the plugin code goes.
The MiniProject2Plugin-class is imported from both run_plugin.py and run_debug.py
"""
import sys
import logging
from webgme_bindings import PluginBase

# Setup a logger
logger = logging.getLogger('MiniProject2Plugin')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)  # By default it logs to stderr..
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class MiniProject2Plugin(PluginBase):
    def main(self):
        # import additional classes
        import time
        import json as json_maker

        # plugin start time
        start = time.time()

        # retrieve instance properties
        core = self.core
        active_node = self.active_node

        # task1
        model_task1 = {'name': core.get_attribute(active_node, 'name'), 'children': {}}
        self.recursive_fill_composition(core, logger, json_maker, active_node, model_task1)
        task1 = json_maker.dumps(model_task1, indent=4, separators=(',', ': '))
        logger.info(task1)

        # task2
        model_task2 = self.build_meta_node_json(core, active_node)
        task2 = json_maker.dumps(model_task2, indent=4, separators=(',', ': '))
        logger.info(task2)

        # save the task outputs
        self.save_code(task1, task2)

        # plugin end time
        end = time.time()

        # print plugin execution time
        logger.info('ELAPSED TIME: ' + str(end - start))

    def save_code(self, task1, task2):
        artifact_hash = self.add_artifact('MiniProject2', {
            'tree.json': task1,
            'meta.json': task2
        })
        logger.info('The artifact is stored under hash: {0}'.format(artifact_hash))

    # loops through children of a node and calls a corresponding dictionary building function
    def recursive_fill_composition(self, core, logger, json_maker, node, model):
        children = core.load_children(node)
        logger.info(children)
        for child in children:
            if core.is_connection(child):
                # logger.info('Connection: ' + core.get_attribute(child, 'name') + ' RelID: ' + core.get_relid(child))
                model['children'].update(self.build_connection_json_dict(core, logger, json_maker, child, model))
            else:
                # logger.info('Node: ' + core.get_attribute(child, 'name') + ' RelID: ' + core.get_relid(child))
                model['children'].update(self.build_node_json_dict(core, logger, json_maker, child, model))

    # builds a dictionary for nodes
    def build_node_json_dict(self, core, logger, json_maker, node, model):
        name = core.get_attribute(node, 'name')
        isMeta = core.is_meta_node(node)
        metaType = core.get_attribute(core.get_meta_type(node), 'name')
        relid = core.get_relid(node)

        node_json = {relid: {'name': name, 'isMeta': isMeta, 'metaType': metaType, 'children': {}}}

        self.recursive_fill_composition(core, logger, json_maker, node, node_json[relid])

        return node_json

    # builds a dictionary for connection
    def build_connection_json_dict(self, core, logger, json_maker, connection, model):
        name = core.get_attribute(connection, 'name')
        isMeta = core.is_meta_node(connection)
        metaType = core.get_attribute(core.get_meta_type(connection), 'name')
        relid = core.get_relid(connection)
        src = core.load_pointer(connection, 'src')
        dst = core.load_pointer(connection, 'dst')
        if src != None:
            srcNode = core.get_attribute(core.get_parent(src), 'name')
        else:
            srcNode = 'null'
        if dst != None:
            dstNode = core.get_attribute(core.get_parent(dst), 'name')
        else:
            dstNode = 'null'

        connection_json = {
            relid: {'name': name, 'isMeta': isMeta, 'metaType': metaType, 'guard': 'null', 'src': srcNode,
                    'dst': dstNode}}

        return connection_json

    # builds array of meta node dictionaries
    def build_meta_node_json(self, core, node):
        model_task2 = []
        metaNodesDict = core.get_all_meta_nodes(node)
        for path in metaNodesDict:
            meta_node = metaNodesDict[path]
            meta_node_path = path
            meta_node_name = core.get_attribute(meta_node, 'name')
            meta_node_children = core.load_children(meta_node)
            if meta_node_children is not None:
                nbr_of_children = len(meta_node_children)
            else:
                nbr_of_children = 0
            meat_node_base = core.get_base(meta_node)
            if meat_node_base is not None:
                meta_node_base_name = core.get_attribute(meat_node_base, 'name')
            else:
                meta_node_base_name = 'null'
            meat_node_json = {'name': meta_node_name, 'path': meta_node_path, 'nbrOfChildren': nbr_of_children,
                              'base': meta_node_base_name}
            model_task2.append(meat_node_json)
        return model_task2
