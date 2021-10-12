"""
utils.py
A set of utils and functions used in this workflow
"""

def get_follower_gids(followerList):
    gidList=[]
    for element in followerList:
        gidList.append(element['gid'])

    gids = ",".join(gidList)

    return gids