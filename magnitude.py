# Number of members in each role (original, cumulative data)
# E.g., Mag 1.0 count includes everyone with Mag 1.0 and above (2, 3, .. 9).
DISTRIBUTION_ORIGINAL = [
    ("Verified", 46349),
    ("Magnitude 1.0", 996),
    ("Magnitude 2.0", 32),
    ("Magnitude 3.0", 1),
    ("Magnitude 4.0", 0),
    ("Magnitude 5.0", 0),
    ("Magnitude 6.0", 0),
    ("Magnitude 7.0", 0),
    ("Magnitude 8.0", 0),
    ("Magnitude 9.0", 0),
]

# Assembly of leaders and mods
N_ASSEMBLY = 7

# Number of weeks remaining to reach the target distribution
N_WEEKS_TOTAL = 24

# Number of weeks passed since March 17th, 2025
N_WEEKS_PASSED = 0


def calculate_exclusive_counts(distribution_original):
    """
    Calculates the number of members exclusive to each role
    (possessing only that specific role) based on the original cumulative data.
    Correct Logic (for Cumulative Data):
    - Exclusive Mag 9 = Original Mag 9
    - Exclusive Mag 8 = Original Mag 8 - Original Mag 9
    - Exclusive Mag 7 = Original Mag 7 - Original Mag 8
    - ...
    - Exclusive Mag 1 = Original Mag 1 - Original Mag 2
    """
    exclusive_counts = {}
    # Copy original data to a dictionary (excluding Verified)
    original_counts = {name: count for name, count in distribution_original[1:]}
    # Get the Verified count
    exclusive_counts["Verified"] = distribution_original[0][1]

    # Iterate downwards starting from the highest magnitude
    magnitude_names_desc = [f"Magnitude {i}.0" for i in range(9, 0, -1)] # 9.0, 8.0, ..., 1.0

    for i in range(len(magnitude_names_desc)):
        current_mag_name = magnitude_names_desc[i] # E.g., Mag 8.0
        # Find the name of the next higher magnitude (Mag 9 for Mag 8, Mag 2 for Mag 1)
        # The highest magnitude (Mag 9) has no higher magnitude (None)
        higher_mag_name = magnitude_names_desc[i-1] if i > 0 else None # E.g., Mag 9.0

        current_original_count = original_counts.get(current_mag_name, 0)

        # If there is a higher magnitude (i.e., for Mag 1-8), subtract its count
        if higher_mag_name:
             higher_original_count = original_counts.get(higher_mag_name, 0)
             exclusive_count = current_original_count - higher_original_count
        else: # Special case for Magnitude 9.0 (highest level)
            exclusive_count = current_original_count

        # Prevent negative counts (in case of data inconsistency)
        exclusive_counts[current_mag_name] = max(0, exclusive_count)

    # Create a new distribution list containing the calculated exclusive counts
    # Keep the order the same as the original DISTRIBUTION (Verified, Mag 1.0 to 9.0)
    distribution_exclusive = [("Verified", exclusive_counts["Verified"])]
    for i in range(1, 10):
        mag_name = f"Magnitude {i}.0"
        distribution_exclusive.append((mag_name, exclusive_counts.get(mag_name, 0)))

    return distribution_exclusive


def calculate_nominations(n_verified, n_current_exclusive, i, n_assembly):
    """
    Calculates the target count for a specific role and the number of
    nominations per assembly member. n_current_exclusive is the count
    of members exclusive to that role (calculated using cumulative logic).
    """
    inertia = max(N_WEEKS_TOTAL - N_WEEKS_PASSED, 0)
    dropoff = 2 + 0.2 * inertia
    target = int(n_verified // dropoff**i)
    total_nominations = target - n_current_exclusive
    nominations = max(0, total_nominations // n_assembly)
    return target, nominations


def main():
    # First, calculate the exclusive member counts for each role (using cumulative data logic)
    distribution_exclusive = calculate_exclusive_counts(DISTRIBUTION_ORIGINAL)
    exclusive_counts_dict = {name: count for name, count in distribution_exclusive}

    # --- NEW: Print Calculated Exclusive Counts ---
    print(f"\n{'='*60}")
    print(f"CALCULATED EXCLUSIVE MEMBER COUNTS".center(60))
    print('='*60)
    print(f"{'Role':<15} {'Exclusive Count':>15}")
    print('-'*60)
    # We can skip the Verified role and print only Magnitude roles
    # Or print all: for name, count in distribution_exclusive:
    for name, count in distribution_exclusive[1:]: # Only Magnitude roles
        print(f"{name:<15} {count:>15,d}")
    print('='*60)
    # --- End: Print Calculated Exclusive Counts ---


    print(f"\n{'='*60}")
    print(f"WEEK {N_WEEKS_PASSED} NOMINATION CALCULATION".center(60))
    print(f"(Using 'Exclusive Count' from Cumulative Data)".center(60))
    print('='*60)

    # Print headers
    print(f"{'Role':<15} {'Target':>10} {'Current (Exc.)':>15} {'Nominations':>12}")
    print('-'*60)

    # Calculate and print for each Magnitude role
    n_verified = exclusive_counts_dict["Verified"]
    for i in range(1, len(distribution_exclusive)): # Start from 1 (Magnitude 1.0)
        name = distribution_exclusive[i][0]
        # Get the exclusive count we already calculated from the dictionary
        n_current_exclusive = exclusive_counts_dict[name]

        # Calculate target and nominations
        target, nominations = calculate_nominations(
            n_verified, n_current_exclusive, i, N_ASSEMBLY)

        # Print results formatted
        print(f"{name:<15} {target:>10,d} {n_current_exclusive:>15,d} {nominations:>12,d}")

    print('='*60 + '\n')


if __name__ == "__main__":
    main()
