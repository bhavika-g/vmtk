##Define voronoi diagram
##Set radius thresholds to get a reduced voronoi
##Find closest points on the reduced voronoi from the original voronoi 
##Use the obtained closest points for endpoint detection 

import vtk 
import numpy as np 
import slicer


voronoi_node = slicer.util.getNode('Voronoi diagram')
voronoi = voronoi_node.GetPolyData()
radius_threshold= 5
threshold_filter = vtk.vtkThreshold()
threshold_filter.SetInputData(voronoi)
threshold_filter.SetLowerThreshold(radius_threshold)
threshold_filter.SetUpperThreshold(200)   # Assuming scalar values represent the radius
threshold_filter.Update()


surface_filter = vtk.vtkDataSetSurfaceFilter()
surface_filter.SetInputData(threshold_filter.GetOutput())
surface_filter.Update()

reduced_voronoi = surface_filter.GetOutput()

modelNode = slicer.vtkMRMLModelNode()
modelNode.SetName("ReducedVoronoiModel")
modelNode.SetAndObservePolyData(reduced_voronoi)


slicer.mrmlScene.AddNode(modelNode)


modelDisplayNode = slicer.vtkMRMLModelDisplayNode()
slicer.mrmlScene.AddNode(modelDisplayNode)
modelNode.SetAndObserveDisplayNodeID(modelDisplayNode.GetID())
modelDisplayNode.SetColor(1, 0, 0)   

locator = vtk.vtkPointLocator()
locator.SetDataSet(reduced_voronoi)
locator.BuildLocator()

closest_points = []
for i in range(voronoi.GetNumberOfPoints()):
    point = voronoi.GetPoint(i)
    closest_point_id = locator.FindClosestPoint(point)
    closest_point = reduced_voronoi.GetPoint(closest_point_id)
    closest_points.append(closest_point)

markupsNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsFiducialNode')
markupsNode.SetName('Complete Endpoints')


for point in closest_points:
    markupsNode.AddControlPoint(point[0], point[1], point[2])


# adjusted_endpoints= []
# for point in initial_endpoints:
#     closest_point_id = locator.FindClosestPoint(point)
#     closest_point_coords = threshold_filter.GetOutput().GetPoint(closest_point_id)
#     adjusted_endpoints.append(closest_point_coords)

# adjusted_endpoints= np.concatenate((initial_endpoints, adjusted_endpoints))
# #adjusted_endpoints= initial_endpoints+adjusted_endpoints
# distance_threshold= 0.1
# i=0

# while i < (len(adjusted_endpoints)):
#         for j in range(i + 1, len(adjusted_endpoints)):
#             print(i,j)
#             distance = vtk.vtkMath.Distance2BetweenPoints(adjusted_endpoints[i], adjusted_endpoints[j])
#             if distance < distance_threshold:  # Square the threshold for efficiency (avoiding sqrt)
#                 # For simplicity, just remove the second point. 
#                 # You can replace this with logic to adjust the point if needed.
#                 #del adjusted_endpoints[j]
#                 adjusted_endpoints = np.delete(adjusted_endpoints, j, axis=0)

#                 j -= 1
#         i += 1



# markupsNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsFiducialNode')
# markupsNode.SetName('Complete Endpoints')


# for point in adjusted_endpoints:
#     markupsNode.AddControlPoint(point[0], point[1], point[2])

# #for point in initial_endpoints:
#     #markupsNode.AddControlPoint(point[0], point[1], point[2])


# markupsNode.GetDisplayNode().SetVisibility(True)


