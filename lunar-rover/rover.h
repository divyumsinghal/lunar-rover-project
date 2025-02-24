#pragma once

#include <memory>
#include <string>
#include <vector>

class Rover {
 public:
  // Constructor and Destructor
  Rover(int id, double latitude, double longitude);
  ~Rover();

  // Movement Controls
  void moveForward(double distance);
  void moveBackward(double distance);
  void turnLeft(double angle);
  void turnRight(double angle);
  void stop();

  // Sensor Data Collection
  std::vector<double> getSensorData();
  std::string getCameraFeed();

  // Communication
  void sendDataToEarth(const std::string& data);
  std::string receiveCommand();
  void discoverNearbyRovers();
  void negotiateWithRovers();
  void establishAgreement();
  void performCollaborativeAction();

  // Getters
  int getID() const;
  double getLatitude() const;
  double getLongitude() const;

 private:
  int roverID;
  double latitude;
  double longitude;

  // Networking attributes
  std::string networkAddress;
  int communicationPort;

  // Helper methods
  std::string serializeData(const std::vector<double>& data);
  std::vector<double> deserializeData(const std::string& data);
};