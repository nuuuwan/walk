import sys

from walk import Walk

if __name__ == '__main__':
    theta_deg = int(sys.argv[1])
    Walk.generate(theta_deg)
