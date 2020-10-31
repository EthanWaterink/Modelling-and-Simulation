from models.traffic_light_models.traffic_light_models import *


class GlobalOptimum(TrafficLightModel):
    """
    The global optimum model with priority and distributed incoming vehicles.
    """
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
            lane_extra = distribute()

            # Determine the lane with the highest priority
            for lane_test in lanes:
                if len(lane_test.queue) + lane_extra[lane_test] > max_queue_length:
                    max_lane = lane_test
                    max_queue_length = len(lane_test.queue)

            return max_lane

        def distribute():
            """
            For each incoming road, equally distribute the incoming vehicles over the lanes.
            """
            # A dictionary{Lane, float} to store the extra weight for that lane.
            lane_extra = {}
            for road in intersection.incoming_roads.values():
                num_lanes = len(road.lanes)
                add_per_lane = len(road.last_section()) / num_lanes
                for lane_inc in road.lanes.values():
                    lane_extra[lane_inc] = add_per_lane
            return lane_extra

        # All traffic lights are set to RED.
        all_traffic_lights_red(intersection)
        # Initialize the options list, which contains the lanes whose traffic lights can be set the GREEN
        options: [Lane] = intersection.get_all_lanes_traffic_lights().copy()

        # Loop while there are still options. Note that the options list will contain at most 4 lanes because for each
        # direction there is only one outgoing lane
        while len(options) > 0:
            # Find the lane with the highest priority
            highest_priority_lane = get_highest_priority_lane(options)
            # Remove it from the options list, since it will be set to GREEN and is no longer an option
            options.remove(highest_priority_lane)
            # Remove all the conflicting lanes
            for lane in find_conflicts(options, highest_priority_lane):
                options.remove(lane)
            # Set the highest priority lane to GREEN
            highest_priority_lane.set_traffic_light_state(Light.GREEN)
