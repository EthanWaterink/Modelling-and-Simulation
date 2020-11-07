from models.traffic_light_models.traffic_light_models import *


class GlobalOptimum(TrafficLightModel):
    """
    The global optimum model with priority and distributed incoming vehicles.
    """

    def setup(self, grid):
        pass

    def update(self, intersection: Intersection):
        """
        Update the intersection with the Global Optimum model.
        """
        def get_highest_priority_lane(lanes: [Lane]):
            """
            Return the lane with the highest priority, which is the one with the most vehicles waiting
            """
            max_lane = None
            max_queue_length = -1

            # Get the extra weights for the lanes
            lanes_extra = distribute()

            # Determine the lane with the highest priority
            for lane in lanes:
                if len(lane.queue) + lanes_extra[lane] > max_queue_length:
                    max_lane = lane
                    max_queue_length = len(lane.queue)

            return max_lane

        def distribute():
            """
            For each incoming road, equally distribute the incoming vehicles over the lanes.
            """
            # A dictionary{Lane, float} to store the extra weight for that lane.
            lanes_extra = {}
            for road in intersection.incoming_roads.values():
                num_lanes = len(road.lanes)
                add_per_lane = len(road.last_section()) / num_lanes
                for lane in road.lanes.values():
                    lanes_extra[lane] = add_per_lane
            return lanes_extra

        # All traffic lights are set to RED.
        all_traffic_lights_red(intersection)
        # Initialize the options list, which contains the lanes whose traffic lights can be set the GREEN
        options = intersection.get_all_lanes_with_traffic_lights()

        # Loop while there are still options. Note that the options list will contain at most 4 lanes because for each
        # direction there is only one outgoing lane
        while len(options) > 0:
            # Find the lane with the highest priority
            highest_priority_lane = get_highest_priority_lane(options)
            # Set the highest priority lane to GREEN
            highest_priority_lane.turn_green()
            # Remove it from the options list, since it will be set to GREEN and is no longer an option
            options.remove(highest_priority_lane)
            # Remove all the conflicting lanes
            options = find_non_conflicting(highest_priority_lane, options)
