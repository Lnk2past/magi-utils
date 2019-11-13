import xml.etree.ElementTree as ElementTree
from re import match

from common.helpers import overwrite_prop, get_env


def do_property_overrides( hbase_site: ElementTree, hdfs_props: dict ) -> ElementTree:
    hbase_root_dir = hdfs_props[ "HBASE_ROOT_DIR" ] if "HBASE_ROOT_DIR" in hdfs_props.keys() else None
    zookeeper_host = hdfs_props[ "HBASE_ZOOKEEPER_HOST" ] if "HBASE_ZOOKEEPER_HOST" in hdfs_props.keys() else None
    zookeeper_port = hdfs_props[ "HBASE_ZOOKEEPER_PORT" ] if "HBASE_ZOOKEEPER_PORT" in hdfs_props.keys() else None
    if hbase_root_dir is not None:
        print( f"reset hbase root.dir {hbase_root_dir}" )
        if match( "hdfs:\/\/[a-zA-Z0-9.-]+(:\d{0,5})?\/[a-zA-Z0-9.-]+", hbase_root_dir ):
            overwrite_prop( hbase_site, "hbase.rootdir", hbase_root_dir )  # careful this mutates core_site
        else:
            print( f"invalid HBASE_ROOT_DIR value : {hbase_root_dir}" )
            exit( 1 )
    if zookeeper_host is not None:
        print( f"reset zk host {zookeeper_host}" )
        overwrite_prop( hbase_site, "hbase.zookeeper.quorum", zookeeper_host )
    if zookeeper_port is not None:
        print( "reset namenode name" )
        overwrite_prop( hbase_site, "hbase.zookeeper.property.clientPort", zookeeper_port )
    return hbase_site


def process( core_site: ElementTree ) -> ElementTree:
    hbase_props = get_env( "HBASE_" )
    if len( hbase_props ) > 0:
        updated_core_site = do_property_overrides( core_site, hbase_props )
        return updated_core_site