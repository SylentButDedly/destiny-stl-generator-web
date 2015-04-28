import io
import os
import json
import urllib
import zipfile

import DataParse
import DestinyGeometry

bungieUrlPrefix = "http://www.bungie.net"
bungieGeometryPrefix = "/common/destiny_content/geometry/platform/mobile/geometry/"

class DestinyModel(object):
    def __init__(self, name, jsonData):
        self.geometry = []
        self.name = name
        
        # Load the json file
        self.json = jsonData
        
        print("Processing geometries...")
        
        if "[Male]" in name:
            # Parse all the geometry indices for male items and parse the geometries
            for geometryIndex in self.json["content"][0]["male_index_set"]["geometry"]:
                geometryFile = self.json["content"][0]["geometry"][geometryIndex]
                path = bungieUrlPrefix+bungieGeometryPrefix+geometryFile
                print("Geometry file: "+path)
                response = urllib.request.urlopen(path)
                data = DataParse.DataParse(response.read())
                self.geometry.append(DestinyGeometry.parse(data))
        elif "[Female]" in name:
            # Parse all the geometry indices for female items and parse the geometries
            for geometryIndex in self.json["content"][0]["female_index_set"]["geometry"]:
                geometryFile = self.json["content"][0]["geometry"][geometryIndex]
                path = bungieUrlPrefix+bungieGeometryPrefix+geometryFile
                print("Geometry file: "+path)
                response = urllib.request.urlopen(path)
                data = DataParse.DataParse(response.read())
                self.geometry.append(DestinyGeometry.parse(data))
        else:
            # Get the geometry file names from the json and parse the geometries
            for geometryFile in self.json["content"][0]["geometry"]:
                path = bungieUrlPrefix+bungieGeometryPrefix+geometryFile
                print("Geometry file: "+path)
                response = urllib.request.urlopen(path)
                data = DataParse.DataParse(response.read())
                self.geometry.append(DestinyGeometry.parse(data))
        
        print("Done processing geometries...")
        return
    
    def generate(self, filePathStl, filePathZip):        
        # Open stl and zip files
        fStl = open(filePathStl, 'w')
        fZip = zipfile.ZipFile(filePathZip, 'w', zipfile.ZIP_DEFLATED)
         
        # Generate stl data for each geometry
        for geometry in self.geometry:
            status = geometry.generate(fStl, fZip)
            if status == False:
                # Something went wrong, cleanup the file and return
                fo.close()
                return "Unable to parse request item geometry"
            
        print("Wrote output file "+filePathStl)
        
        # Close stl and zip files
        fStl.close()
        fZip.close()
            
        return
    